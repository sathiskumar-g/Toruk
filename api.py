"""
Simple Flask API for TORUKMACTO Reddit Research
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
from datetime import datetime
import os
from pathlib import Path

# Import the batch research function
from scrapers import RedditScraper
from processors import ProblemExtractor, OpportunityScorer

app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/api/keywords', methods=['GET'])
def get_keywords():
    """Get current keywords from research_keywords.json"""
    try:
        with open('research_keywords.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Support both old and new key for backward compatibility
            keywords = data.get('keywords')
            if keywords is None:
                keywords = data.get('reddit_keywords', [])
            return jsonify({'keywords': keywords})
    except FileNotFoundError:
        return jsonify({'keywords': []})

@app.route('/api/keywords', methods=['POST'])
def save_keywords():
    """Save keywords to research_keywords.json"""
    data = request.json
    keywords = data.get('keywords', [])
    source = data.get('source', None)
    out = {'keywords': keywords}
    if source:
        out['source'] = source
    with open('research_keywords.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)
    return jsonify({'success': True, 'keywords': keywords})

@app.route('/api/research', methods=['POST'])
def run_research():
    """Run batch Reddit research"""
    data = request.json
    keywords = data.get('keywords', [])
    limit = data.get('limit', 5)
    source = data.get('source', 'reddit')

    if not keywords:
        return jsonify({'error': 'No keywords provided'}), 400

    # Save keywords first
    with open('research_keywords.json', 'w', encoding='utf-8') as f:
        json.dump({'keywords': keywords, 'source': source}, f, indent=2)

    # Select scraper
    if source == 'reddit':
        from scrapers.reddit import RedditScraper
        scraper = RedditScraper()
        fetch_comments = True
    elif source == 'hackernews':
        from scrapers.hackernews import HackerNewsScraper
        scraper = HackerNewsScraper()
        fetch_comments = False
    elif source == 'github':
        from scrapers.github_issues import GitHubIssuesScraper
        scraper = GitHubIssuesScraper()
        fetch_comments = False
    else:
        return jsonify({'error': f'Unknown source: {source}'}), 400

    extractor = ProblemExtractor()
    scorer = OpportunityScorer()

    all_opportunities = []
    keyword_results = {}

    for idx, keyword in enumerate(keywords, 1):
        print(f"\n[{idx}/{len(keywords)}] Processing: {keyword} (source: {source})")
        try:
            # Search selected source
            if source == 'reddit':
                results = scraper.scrape_ai_saas_problems(keyword, limit=limit)
                # Fetch comments for top posts (Reddit only)
                if fetch_comments and results:
                    for post in results[:3]:
                        try:
                            comments = scraper.get_post_comments(post['url'], limit=5)
                            post['top_comments'] = comments
                        except Exception as e:
                            print(f"⚠️ Skipping comments for post: {e}")
                            post['top_comments'] = []
            else:
                results = scraper.scrape(keyword, limit=limit)

            # Extract and score
            problems = extractor.extract_problems(results)
            opportunities = scorer.score_problems(problems)

            # Add to aggregate results
            keyword_results[keyword] = {
                "total_posts": len(results),
                "problems_found": len(problems),
                "opportunities_found": len(opportunities),
                "top_opportunity_score": opportunities[0].get("opportunity_score", {}).get("total", 0) if opportunities else 0
            }

            # Tag opportunities with keyword and source
            for opp in opportunities:
                opp["research_keyword"] = keyword
                opp["source"] = source
            all_opportunities.extend(opportunities)

            print(f"✅ Completed {keyword}: {len(opportunities)} opportunities")
        except Exception as e:
            print(f"⚠️ Error processing '{keyword}': {e}")
            # Add empty result for this keyword but continue
            keyword_results[keyword] = {
                "total_posts": 0,
                "problems_found": 0,
                "opportunities_found": 0,
                "top_opportunity_score": 0,
                "error": str(e)
            }
            continue  # Move to next keyword

    # Sort all opportunities by score
    all_opportunities.sort(
        key=lambda x: x.get("opportunity_score", {}).get("total", 0),
        reverse=True
    )

    # Create final output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = {
        "research_completed_at": datetime.now().isoformat(),
        "keywords_file": "research_keywords.json",
        "total_keywords": len(keywords),
        "keyword_summary": keyword_results,
        "total_opportunities": len(all_opportunities),
        "top_10_opportunities": all_opportunities[:10],
        "all_opportunities": all_opportunities
    }

    # Save to file
    os.makedirs('data', exist_ok=True)
    filename = f"data/reddit_research_final_{timestamp}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    return jsonify({
        'success': True,
        'results': output,
        'filename': filename
    })

@app.route('/api/results', methods=['GET'])
def get_latest_results():
    """Get the latest research results"""
    data_dir = Path('data')
    if not data_dir.exists():
        return jsonify({'error': 'No results found'}), 404
    
    # Find latest results file
    result_files = sorted(data_dir.glob('reddit_research_final_*.json'), reverse=True)
    if not result_files:
        return jsonify({'error': 'No results found'}), 404
    
    with open(result_files[0], 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    return jsonify(results)

if __name__ == '__main__':
    print("🚀 Starting TORUKMACTO Research API...")
    print("📡 Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)

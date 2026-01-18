
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

# Place the /api/saved/<filename> endpoint BEFORE the static catch-all route
@app.route('/api/saved/<filename>', methods=['GET'])
def get_saved_file(filename):
    """Serve a saved research JSON file from data/saved."""
    from flask import abort
    import urllib.parse
    print(f"[DEBUG] Looking for file start")
    # Decode URL-encoded filename
    filename = urllib.parse.unquote(filename)
    import os
    save_dir = Path(os.path.abspath(os.path.join(os.getcwd(), 'mock', 'torukmacto', 'data', 'saved')))
    file_path = save_dir / filename
    print(f"[DEBUG] Looking for file: {file_path}")
    print(f"[DEBUG] Exists: {file_path.exists()}, Is file: {file_path.is_file()}")
    if not file_path.exists() or not file_path.is_file():
        print("[DEBUG] 404: File not found")
        abort(404)
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("[DEBUG] File loaded successfully")
    return jsonify(data)


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

# Register /api/list_saved_files at the top level
@app.route('/api/list_saved_files', methods=['GET'])
def list_saved_files():
    """Return a list of saved research result files with display names."""
    save_dir = Path('data/saved')
    files = list(save_dir.glob('*.json'))
    result = []
    for f in files:
        fname = f.name
        match = None
        # Match: name_YYYYMMDD_HHMMSS.json
        import re
        match = re.match(r'^(.*)_([0-9]{8}_[0-9]{6})\.json$', fname)
        display = fname
        if match:
            name = match.group(1)
            ts = match.group(2)
            year, month, day = ts[:4], ts[4:6], ts[6:8]
            hour, minute, sec = ts[9:11], ts[11:13], ts[13:15]
            formatted = f"{year}-{month}-{day} {hour}:{minute}:{sec}"
            display = f"{name} - {formatted}"
        result.append({"filename": fname, "display": display})
    return jsonify(result)

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

@app.route('/api/save_results', methods=['POST'])
def save_results():
    """Save current research results to the saved folder with a requested filename and timestamp."""
    data = request.json
    results = data.get('results')
    filename = data.get('filename')
    if not results or not filename:
        return jsonify({'error': 'Missing results or filename'}), 400
    # Ensure safe filename (alphanumeric, dash, underscore only)
    import re
    safe_filename = re.sub(r'[^a-zA-Z0-9-_]', '_', filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    save_dir = Path('data/saved')
    save_dir.mkdir(parents=True, exist_ok=True)
    full_filename = save_dir / f"{safe_filename}_{timestamp}.json"
    with open(full_filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    return jsonify({'success': True, 'saved_file': str(full_filename)})

if __name__ == '__main__':
    print("🚀 Starting TORUKMACTO Research API...")
    print("📡 Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)

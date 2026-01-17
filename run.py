#!/usr/bin/env python3
"""
🔍 TORUKMACTO - Problem Research Engine
========================================
Find real, painful, monetizable problems in the AI tools ecosystem.

Usage:
    python run.py search langchain
    python run.py scan --all
    python run.py report

"Toruk Macto" = "Rider of Last Shadow" (Na'vi)
Like seeing from above what others can't see.
"""

import argparse
import json
import sys
from datetime import datetime

from scrapers import HackerNewsScraper, GitHubIssuesScraper, RedditScraper
from processors import ProblemExtractor, OpportunityScorer
from config import TOOLS_TO_MONITOR, PROBLEM_KEYWORDS, GITHUB_REPOS, REDDIT_SUBREDDITS


def search_topic(topic: str, limit: int = 50, include_reddit: bool = True) -> dict:
    """Search for problems related to a specific topic"""
    print(f"\n🔍 SEARCHING: '{topic}'")
    print("=" * 50)
    
    all_results = []
    
    # 1. Search Hacker News
    print("\n📰 Searching Hacker News...")
    hn = HackerNewsScraper()
    hn_results = hn.scrape_topic(topic, PROBLEM_KEYWORDS[:5])
    all_results.extend(hn_results)
    
    # 2. Search GitHub Issues
    print("\n🐙 Searching GitHub Issues...")
    gh = GitHubIssuesScraper()
    gh_results = gh.scrape(f"{topic} bug OR error OR issue", limit=30)
    all_results.extend(gh_results)
    
    # 3. Search Reddit (NEW!)
    if include_reddit:
        print("\n🤖 Searching Reddit...")
        reddit = RedditScraper()
        reddit_results = reddit.scrape_multiple_subreddits(
            query=f"{topic} problem OR issue",
            subreddits=REDDIT_SUBREDDITS[:5],  # Top 5 relevant subreddits
            limit_per_sub=5
        )
        all_results.extend(reddit_results)
    
    print(f"\n📊 Total raw results: {len(all_results)}")
    
    # 3. Extract problems
    print("\n🔬 Extracting problems...")
    extractor = ProblemExtractor()
    problems = extractor.extract_problems(all_results)
    
    # 4. Score opportunities
    print("\n📈 Scoring opportunities...")
    scorer = OpportunityScorer()
    opportunities = scorer.score_problems(problems)
    
    # 5. Print report
    scorer.print_report(top_n=5)
    
    # 6. Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/search_{topic}_{timestamp}.json"
    
    output = {
        "topic": topic,
        "searched_at": datetime.now().isoformat(),
        "raw_results": len(all_results),
        "problems_found": len(problems),
        "top_opportunities": scorer.get_top_opportunities(10)
    }
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {filename}")
    
    return output


def scan_all_tools(limit_per_tool: int = 30) -> dict:
    """Scan all monitored tools for problems"""
    print("\n🚀 FULL SCAN MODE")
    print(f"Scanning {len(TOOLS_TO_MONITOR)} tools...")
    print("=" * 50)
    
    all_opportunities = []
    
    for tool in TOOLS_TO_MONITOR:
        print(f"\n{'='*40}")
        print(f"🔍 Scanning: {tool}")
        print(f"{'='*40}")
        
        try:
            # Quick search for each tool
            hn = HackerNewsScraper()
            results = hn.scrape(f"{tool} problem OR issue OR bug", limit=limit_per_tool)
            
            if results:
                extractor = ProblemExtractor()
                problems = extractor.extract_problems(results)
                
                scorer = OpportunityScorer()
                opportunities = scorer.score_problems(problems)
                
                # Keep top 3 per tool
                top_opps = scorer.get_top_opportunities(3)
                for opp in top_opps:
                    opp["search_tool"] = tool
                all_opportunities.extend(top_opps)
                
                print(f"   Found {len(problems)} problems, {len(top_opps)} top opportunities")
            else:
                print(f"   No results found")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue
    
    # Sort all opportunities by score
    all_opportunities.sort(key=lambda x: x.get("opportunity_score", {}).get("total", 0), reverse=True)
    
    # Print final report
    print("\n" + "=" * 60)
    print("🏆 TOP 10 OPPORTUNITIES ACROSS ALL TOOLS")
    print("=" * 60)
    
    for i, opp in enumerate(all_opportunities[:10], 1):
        score = opp.get("opportunity_score", {}).get("total", 0)
        tool = opp.get("search_tool", "unknown")
        print(f"\n#{i} [{score:.1f}/10] [{tool}]")
        print(f"   {opp.get('problem_statement', 'No statement')[:60]}...")
        print(f"   {opp.get('recommendation', '')}")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/full_scan_{timestamp}.json"
    
    output = {
        "scanned_at": datetime.now().isoformat(),
        "tools_scanned": len(TOOLS_TO_MONITOR),
        "total_opportunities": len(all_opportunities),
        "opportunities": all_opportunities
    }
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Full scan saved to: {filename}")
    
    return output


def scan_github_repos() -> dict:
    """Scan specific GitHub repos for painful issues"""
    print("\n🐙 GITHUB REPOS SCAN")
    print(f"Scanning {len(GITHUB_REPOS)} repositories...")
    print("=" * 50)
    
    all_issues = []
    gh = GitHubIssuesScraper()
    
    for repo in GITHUB_REPOS:
        owner, name = repo.split("/")
        print(f"\n📦 {repo}")
        
        try:
            issues = gh.find_painful_issues(owner, name, min_reactions=5)
            all_issues.extend(issues[:5])  # Top 5 per repo
            print(f"   Found {len(issues)} high-engagement issues")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Extract and score
    if all_issues:
        extractor = ProblemExtractor()
        problems = extractor.extract_problems(all_issues)
        
        scorer = OpportunityScorer()
        opportunities = scorer.score_problems(problems)
        scorer.print_report(top_n=10)
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/github_scan_{timestamp}.json"
        scorer.save_opportunities(filename)
        
        return {"opportunities": opportunities}
    
    return {"opportunities": []}


def search_reddit_problems(problem_keyword: str = None, limit: int = 50) -> dict:
    """
    Search Reddit for AI/SaaS problems using problem keywords
    
    Args:
        problem_keyword: Specific problem keyword (e.g., "frustrating", "doesn't work")
                        If None, searches for general AI tool problems
        limit: Max results
    """
    print("\n🤖 REDDIT PROBLEM SEARCH")
    print("=" * 50)
    
    reddit = RedditScraper()
    
    if problem_keyword:
        print(f"Searching for: '{problem_keyword}' in AI/SaaS subreddits")
        results = reddit.scrape_ai_saas_problems(problem_keyword, limit=limit)
    else:
        print("Searching AI/SaaS subreddits for common problems...")
        # Search for multiple problem patterns
        all_results = []
        problem_patterns = [
            "doesn't work",
            "frustrating",
            "alternative to",
            "biggest problem"
        ]
        
        for pattern in problem_patterns[:2]:  # Limit to avoid too many requests
            results = reddit.scrape_ai_saas_problems(pattern, limit=limit // 2)
            all_results.extend(results)
        
        # Deduplicate
        seen_urls = set()
        results = []
        for item in all_results:
            if item["url"] not in seen_urls:
                seen_urls.add(item["url"])
                results.append(item)
    
    print(f"\n📊 Found {len(results)} Reddit posts")
    
    # Extract and score
    if results:
        extractor = ProblemExtractor()
        problems = extractor.extract_problems(results)
        
        scorer = OpportunityScorer()
        opportunities = scorer.score_problems(problems)
        scorer.print_report(top_n=10)
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/reddit_search_{timestamp}.json"
        
        output = {
            "searched_at": datetime.now().isoformat(),
            "problem_keyword": problem_keyword or "general",
            "raw_results": len(results),
            "problems_found": len(problems),
            "opportunities": opportunities
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {filename}")
        return output
    
    return {"opportunities": []}


def batch_reddit_research(keywords_file: str = "research_keywords.json", limit: int = 50, fetch_comments: bool = True) -> dict:
    """
    Run Reddit research for all keywords in the JSON file
    
    Args:
        keywords_file: Path to JSON file with keyword array
        limit: Max results per keyword
        fetch_comments: Whether to fetch top comments from each post
    """
    print("\n\U0001F680 BATCH REDDIT RESEARCH")
    print("=" * 60)
    
    # Load keywords from file
    try:
        with open(keywords_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            keywords = data.get("reddit_keywords", [])
    except FileNotFoundError:
        print(f"❌ Keywords file not found: {keywords_file}")
        print("💡 Create it with: {'reddit_keywords': ['keyword1', 'keyword2']}")
        return {"error": "File not found"}
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {keywords_file}: {e}")
        return {"error": "Invalid JSON"}
    
    if not keywords:
        print("❌ No keywords found in file")
        return {"error": "No keywords"}
    
    print(f"📋 Loaded {len(keywords)} keywords from {keywords_file}")
    print(f"⏱️  Estimated time: ~{len(keywords) * 15} seconds\n")
    
    # Initialize Reddit scraper
    reddit = RedditScraper()
    extractor = ProblemExtractor()
    scorer = OpportunityScorer()
    
    all_opportunities = []
    keyword_results = {}
    
    # Process each keyword
    for i, keyword in enumerate(keywords, 1):
        if not keyword or keyword.strip() == "":
            continue
            
        print(f"\n{'='*60}")
        print(f"🔍 [{i}/{len(keywords)}] Researching: '{keyword}'")
        print(f"{'='*60}")
        
        try:
            # Search Reddit
            results = reddit.scrape_ai_saas_problems(keyword, limit=limit)
            print(f"📊 Found {len(results)} posts")
            
            # Fetch top comments for each post (optional)
            if fetch_comments and results:
                print(f"💬 Fetching comments from top posts...")
                for post in results[:5]:  # Get comments from top 5 posts
                    comments = reddit.get_post_comments(post['url'], limit=10)
                    post['top_comments'] = comments
            
            # Extract and score
            problems = extractor.extract_problems(results)
            opportunities = scorer.score_problems(problems)
            
            print(f"✅ Extracted {len(problems)} problems from {len(results)} posts")
            
            # Add to aggregate results
            keyword_results[keyword] = {
                "total_posts": len(results),
                "problems_found": len(problems),
                "opportunities_found": len(opportunities),
                "top_opportunity_score": opportunities[0].get("opportunity_score", {}).get("total", 0) if opportunities else 0
            }
            
            # Tag opportunities with keyword and add to aggregate
            for opp in opportunities:
                opp["research_keyword"] = keyword
            all_opportunities.extend(opportunities)
            
        except Exception as e:
            print(f"❌ Error processing '{keyword}': {e}")
            keyword_results[keyword] = {"error": str(e)}
    
    # Create final aggregate report
    print(f"\n\n{'='*60}")
    print("📊 FINAL AGGREGATE REPORT")
    print(f"{'='*60}\n")
    
    # Sort by opportunity score
    all_opportunities.sort(key=lambda x: x.get("opportunity_score", {}).get("total", 0), reverse=True)
    
    # Print summary
    print(f"Total keywords processed: {len(keyword_results)}")
    print(f"Total opportunities found: {len(all_opportunities)}")
    print(f"\nTop opportunities by score:\n")
    
    for i, opp in enumerate(all_opportunities[:10], 1):
        score = opp.get("opportunity_score", {}).get("total", 0)
        keyword = opp.get("research_keyword", "unknown")
        title = opp.get("original_title", "No title")
        print(f"  {i}. [{score:.1f}/10] {title[:50]}...")
        print(f"     Keyword: '{keyword}'")
        print(f"     URL: {opp.get('url', 'N/A')}\n")
    
    # Save final aggregate JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_filename = f"data/reddit_research_final_{timestamp}.json"
    
    final_output = {
        "research_completed_at": datetime.now().isoformat(),
        "keywords_file": keywords_file,
        "total_keywords": len(keywords),
        "keyword_summary": keyword_results,
        "total_opportunities": len(all_opportunities),
        "top_10_opportunities": all_opportunities[:10],
        "all_opportunities": all_opportunities
    }
    
    with open(final_filename, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)
    
    print(f"{'='*60}")
    print(f"✅ Research complete!")
    print(f"💾 Final report saved to: {final_filename}")
    print(f"{'='*60}\n")
    
    return final_output


def quick_demo():
    """Run a quick demo to show the system works"""
    print("\n" + "=" * 60)
    print("🎯 TORUKMACTO - Quick Demo")
    print("=" * 60)
    print("\nThis demo will:")
    print("1. Search Hacker News for 'langchain' problems")
    print("2. Extract and score the problems")
    print("3. Show you the top opportunities")
    print("\n" + "-" * 40)
    
    # Run a quick search
    result = search_topic("langchain", limit=30)
    
    print("\n" + "=" * 60)
    print("✅ Demo complete!")
    print(f"Found {result['problems_found']} problems")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="🔍 TORUKMACTO - Problem Research Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py demo                    # Quick demo with LangChain
  python run.py search "n8n"            # Search for n8n problems
  python run.py search "openai api"     # Search for OpenAI API issues
  python run.py scan --all              # Scan all monitored tools
  python run.py scan --github           # Scan GitHub repos only
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Demo command
    demo_parser = subparsers.add_parser("demo", help="Run a quick demo")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search for problems on a topic")
    search_parser.add_argument("topic", type=str, help="Topic to search for")
    search_parser.add_argument("--limit", type=int, default=50, help="Max results per source")
    search_parser.add_argument("--no-reddit", action="store_true", help="Skip Reddit (faster)")
    
    # Reddit command (NEW!)
    reddit_parser = subparsers.add_parser("reddit", help="Search Reddit for AI/SaaS problems")
    reddit_parser.add_argument("--keyword", type=str, default=None, 
                              help="Problem keyword (e.g., 'frustrating', 'doesn't work')")
    reddit_parser.add_argument("--limit", type=int, default=50, help="Max results")
    
    # Batch Reddit research command (NEW!)
    batch_reddit_parser = subparsers.add_parser("batch-reddit", 
                                                help="Run research for all keywords in research_keywords.json")
    batch_reddit_parser.add_argument("--keywords-file", type=str, default="research_keywords.json",
                                    help="Path to JSON file with keyword array")
    batch_reddit_parser.add_argument("--limit", type=int, default=50, help="Max results per keyword")
    
    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan multiple sources")
    scan_parser.add_argument("--all", action="store_true", help="Scan all monitored tools")
    scan_parser.add_argument("--github", action="store_true", help="Scan GitHub repos only")
    scan_parser.add_argument("--reddit", action="store_true", help="Scan Reddit only")
    
    args = parser.parse_args()
    
    if args.command == "demo":
        quick_demo()
    elif args.command == "search":
        include_reddit = not args.no_reddit
        search_topic(args.topic, args.limit, include_reddit=include_reddit)
    elif args.command == "reddit":
        search_reddit_problems(args.keyword, args.limit)
    elif args.command == "batch-reddit":
        batch_reddit_research(args.keywords_file, args.limit)
    elif args.command == "scan":
        if args.all:
            scan_all_tools()
        elif args.github:
            scan_github_repos()
        elif args.reddit:
            search_reddit_problems(limit=100)
        else:
            print("Please specify --all, --github, or --reddit")
            parser.print_help()
    else:
        parser.print_help()
        print("\n💡 Try: python run.py demo")


if __name__ == "__main__":
    main()

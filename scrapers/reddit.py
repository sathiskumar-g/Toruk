"""
Reddit Scraper (JSON API - No Auth Required!)
Uses Reddit's free JSON API - just add .json to any URL

Reddit paid API costs $0.24/1000 calls, but the JSON endpoints are still free!
Example: https://www.reddit.com/search.json?q=your+query
"""
import requests
from typing import List, Dict, Any
import time
from .base import BaseScraper


class RedditScraper(BaseScraper):
    """
    Scrape Reddit for problem discussions using free JSON API
    
    Uses Reddit's JSON endpoints (no auth needed)
    Rate Limit: Self-imposed (2 seconds between requests to be respectful)
    Auth: None required!
    """
    
    BASE_URL = "https://www.reddit.com"
    
    # AI/SaaS/Automation focused subreddits (kept for optional use)
    TARGET_SUBREDDITS = [
        "artificial",
        "OpenAI",
        "ChatGPT",
        "LangChain",
        "LocalLLaMA",
        "MachineLearning",
        "learnmachinelearning",
        "SaaS",
        "Entrepreneur",
        "startups",
        "Automate",
        "nocode",
        "automation",
        "webdev",
        "technology",
        "programming",
        "Python",
        "AIAgents"
    ]
    
    def __init__(self):
        super().__init__("reddit")
        self.session = requests.Session()
        # Mimic a real browser for JSON API
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ProblemResearchBot/1.0",
            "Accept": "application/json",
        })
        self.request_delay = 3  # Increased delay between requests (seconds)
        self.last_request_time = 0
        
    def scrape(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search ALL of Reddit for posts matching the query (using JSON API)
        
        Args:
            query: Search term (e.g., "I wish there was a tool for AI")
            limit: Max results
        """
        print(f"🔍 Searching ALL of Reddit for: '{query}'")
        
        all_results = []
        after = None  # Pagination cursor
        
        while len(all_results) < limit:
            url = f"{self.BASE_URL}/search.json"
            params = {
                "q": query,
                "sort": "relevance",
                "t": "all",  # all time
                "limit": min(100, limit - len(all_results)),  # Reddit max 100 per page
                "raw_json": 1  # Get unescaped JSON
            }
            
            if after:
                params["after"] = after
            
            # Rate limiting: ensure delay between requests
            elapsed = time.time() - self.last_request_time
            if elapsed < self.request_delay:
                time.sleep(self.request_delay - elapsed)
            
            try:
                self.last_request_time = time.time()
                response = self.session.get(url, params=params, timeout=15)
                response.raise_for_status()
                
                data = response.json()
                posts = self._parse_json_response(data)
                
                if not posts:
                    break
                
                all_results.extend(posts)
                print(f"   Found {len(posts)} posts (total: {len(all_results)})")
                
                # Get pagination token
                after = data.get("data", {}).get("after")
                if not after:
                    break
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    print(f"⚠️ Rate limited by Reddit. Waiting 10 seconds...")
                    time.sleep(10)
                    # Don't break, just skip this batch
                else:
                    print(f"❌ HTTP Error: {e}")
                break
            except Exception as e:
                print(f"❌ Error scraping Reddit: {e}")
                break
        
        self.results = all_results[:limit]
        print(f"📊 Total found: {len(self.results)} Reddit posts")
        return self.results
    
    def _parse_json_response(self, data: dict) -> List[Dict[str, Any]]:
        """Parse Reddit JSON API response"""
        posts = []
        
        try:
            children = data.get("data", {}).get("children", [])
            
            for child in children:
                post_data = child.get("data", {})
                
                # Skip non-post items
                if child.get("kind") != "t3":
                    continue
                
                # Extract post data (get full text, not truncated)
                selftext = post_data.get('selftext', '')
                post = {
                    "type": "post",
                    "id": post_data.get("id"),
                    "title": post_data.get("title", ""),
                    "text": f"{post_data.get('title', '')} {selftext}",  # Full text, no truncation
                    "url": f"https://www.reddit.com{post_data.get('permalink', '')}",
                    "subreddit": post_data.get("subreddit", "unknown"),
                    "author": post_data.get("author", "unknown"),
                    "points": post_data.get("score", 0),
                    "reactions": post_data.get("score", 0),  # For compatibility
                    "comments": post_data.get("num_comments", 0),
                    "created_at": None,  # Could parse from created_utc if needed
                    "source": "reddit"
                }
                
                posts.append(post)
                
        except Exception as e:
            print(f"❌ Error parsing JSON: {e}")
        
        return posts
    
    def scrape_subreddit(self, subreddit: str, query: str, limit: int = 30) -> List[Dict[str, Any]]:
        """
        Search within a specific subreddit using JSON API
        
        Args:
            subreddit: Subreddit name (e.g., "OpenAI", "SaaS")
            query: Search term
            limit: Max results
        """
        print(f"🔍 Searching r/{subreddit} for: '{query}'")
        
        url = f"{self.BASE_URL}/r/{subreddit}/search.json"
        params = {
            "q": query,
            "restrict_sr": "on",  # Search only this subreddit
            "sort": "relevance",
            "t": "all",
            "limit": min(limit, 100),
            "raw_json": 1
        }
        
        try:
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            posts = self._parse_json_response(data)
            
            self.results = posts[:limit]
            print(f"📊 Found {len(self.results)} posts in r/{subreddit}")
            return self.results
            
        except Exception as e:
            print(f"❌ Error scraping r/{subreddit}: {e}")
            return []
    
    def scrape_ai_saas_problems(self, problem_keyword: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search ALL of Reddit for AI/SaaS problems (no subreddit restriction!)
        
        Args:
            problem_keyword: Problem keyword (e.g., "frustrating", "doesn't work")
            limit: Max total results
        """
        # Search with ONE query to avoid rate limiting
        # The keyword itself is enough context
        query = f"{problem_keyword}"
        
        print(f"🔍 Searching Reddit for keyword: '{problem_keyword}'")
        
        try:
            # Single search to avoid multiple API calls
            all_results = self.scrape(query, limit=limit)
        except Exception as e:
            print(f"❌ Failed to search '{problem_keyword}': {e}")
            all_results = []
        
        # Deduplicate by URL
        seen_urls = set()
        unique_results = []
        for item in all_results:
            url = item.get("url")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(item)
        
        self.results = unique_results[:limit]
        print(f"✅ Returned {len(self.results)} unique results for '{problem_keyword}'")
        return self.results
    
    def get_post_comments(self, post_url: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get comments from a specific post using JSON API
        
        Args:
            post_url: Full URL to the Reddit post
            limit: Max comments to fetch
        """
        # Add .json to URL
        json_url = post_url.rstrip('/') + '.json'
        
        # Rate limiting
        elapsed = time.time() - self.last_request_time
        if elapsed < self.request_delay:
            time.sleep(self.request_delay - elapsed)
        
        try:
            self.last_request_time = time.time()
            response = self.session.get(json_url, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            comments = []
            
            # Reddit returns [post_data, comments_data]
            if len(data) >= 2:
                comments_listing = data[1].get("data", {}).get("children", [])
                
                for comment_obj in comments_listing:
                    if comment_obj.get("kind") != "t1":  # t1 = comment
                        continue
                    
                    comment_data = comment_obj.get("data", {})
                    comments.append({
                        "type": "comment",
                        "text": comment_data.get("body", ""),
                        "author": comment_data.get("author", "unknown"),
                        "points": comment_data.get("score", 0),
                        "reactions": comment_data.get("score", 0),
                        "source": "reddit"
                    })
                    
                    if len(comments) >= limit:
                        break
            
            return comments
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print(f"⚠️ Rate limited fetching comments. Skipping...")
            else:
                print(f"❌ Error fetching comments: {e}")
            return []
        except Exception as e:
            print(f"❌ Error fetching comments: {e}")
            return []


# Quick test
if __name__ == "__main__":
    scraper = RedditScraper()
    
    # Test: Search ALL of Reddit for a problem
    results = scraper.scrape("I wish there was a tool for AI", limit=10)
    
    print("\n" + "="*60)
    print("Top 5 Results:")
    for i, post in enumerate(results[:5], 1):
        print(f"\n{i}. r/{post['subreddit']} - {post['title'][:60]}...")
        print(f"   Points: {post['points']} | Comments: {post['comments']}")
        print(f"   URL: {post['url']}")

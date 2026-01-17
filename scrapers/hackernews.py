"""
Hacker News Scraper
Uses the FREE HN Algolia API - no auth required!
https://hn.algolia.com/api

This is the BEST free source for developer pain points.
"""
import requests
from typing import List, Dict, Any
from datetime import datetime
from .base import BaseScraper


class HackerNewsScraper(BaseScraper):
    """
    Scrape Hacker News for problem discussions
    
    API Docs: https://hn.algolia.com/api
    Rate Limit: Very generous (10,000 requests/hour)
    Auth: None required!
    """
    
    BASE_URL = "https://hn.algolia.com/api/v1"
    
    def __init__(self):
        super().__init__("hackernews")
        
    def scrape(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search HN for posts/comments containing the query
        
        Args:
            query: Search term (e.g., "langchain problem", "n8n frustrating")
            limit: Max results (API allows up to 1000 per page)
        """
        print(f"🔍 Searching Hacker News for: '{query}'")
        
        # Search both stories and comments
        stories = self._search_stories(query, limit // 2)
        comments = self._search_comments(query, limit // 2)
        
        self.results = stories + comments
        print(f"📊 Found {len(self.results)} results ({len(stories)} stories, {len(comments)} comments)")
        
        return self.results
    
    def _search_stories(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Search story titles and content"""
        url = f"{self.BASE_URL}/search"
        params = {
            "query": query,
            "tags": "story",
            "hitsPerPage": min(limit, 100),
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for hit in data.get("hits", []):
                results.append({
                    "type": "story",
                    "id": hit.get("objectID"),
                    "title": hit.get("title", ""),
                    "text": hit.get("title", "") + " " + (hit.get("story_text") or ""),
                    "url": f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
                    "author": hit.get("author"),
                    "points": hit.get("points", 0),
                    "comments": hit.get("num_comments", 0),
                    "created_at": hit.get("created_at"),
                    "source": "hackernews"
                })
            return results
            
        except Exception as e:
            print(f"❌ Error searching stories: {e}")
            return []
    
    def _search_comments(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Search comments - often contain the best pain points!"""
        url = f"{self.BASE_URL}/search"
        params = {
            "query": query,
            "tags": "comment",
            "hitsPerPage": min(limit, 100),
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for hit in data.get("hits", []):
                comment_text = hit.get("comment_text", "")
                # Skip very short comments
                if len(comment_text) < 50:
                    continue
                    
                results.append({
                    "type": "comment",
                    "id": hit.get("objectID"),
                    "title": f"Comment on: {hit.get('story_title', 'Unknown')}",
                    "text": comment_text,
                    "url": f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
                    "parent_url": f"https://news.ycombinator.com/item?id={hit.get('story_id')}",
                    "author": hit.get("author"),
                    "points": hit.get("points", 0),
                    "created_at": hit.get("created_at"),
                    "source": "hackernews"
                })
            return results
            
        except Exception as e:
            print(f"❌ Error searching comments: {e}")
            return []
    
    def scrape_topic(self, tool_name: str, problem_keywords: List[str] = None) -> List[Dict[str, Any]]:
        """
        Smart search for problems related to a specific tool
        
        Example: scrape_topic("langchain", ["error", "bug", "frustrating"])
        """
        if problem_keywords is None:
            problem_keywords = ["problem", "issue", "bug", "error", "frustrating", "doesn't work"]
        
        all_results = []
        
        # Search for tool + each problem keyword
        for keyword in problem_keywords[:3]:  # Limit to avoid rate limits
            query = f"{tool_name} {keyword}"
            results = self.scrape(query, limit=30)
            all_results.extend(results)
        
        # Deduplicate by ID
        seen_ids = set()
        unique_results = []
        for item in all_results:
            if item["id"] not in seen_ids:
                seen_ids.add(item["id"])
                unique_results.append(item)
        
        self.results = unique_results
        return unique_results


# Quick test
if __name__ == "__main__":
    scraper = HackerNewsScraper()
    
    # Test basic search
    results = scraper.scrape("langchain frustrating", limit=20)
    
    for r in results[:5]:
        print(f"\n📌 {r['type'].upper()}: {r['title'][:60]}...")
        print(f"   Points: {r['points']} | URL: {r['url']}")
    
    # Save results
    scraper.save_results()

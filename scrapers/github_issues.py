"""
GitHub Issues Scraper
Uses GitHub's free API - 60 requests/hour without auth
With a token: 5000 requests/hour

Perfect for finding real user problems in open source tools!
"""
import requests
from typing import List, Dict, Any, Optional
from .base import BaseScraper


class GitHubIssuesScraper(BaseScraper):
    """
    Scrape GitHub Issues for bug reports and feature requests
    
    Rate Limits:
    - Without token: 60 requests/hour
    - With token: 5000 requests/hour
    
    Best for: Finding real user problems in popular tools
    """
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None):
        super().__init__("github_issues")
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
            print("✅ Using authenticated GitHub API (5000 req/hr)")
        else:
            print("⚠️ Using unauthenticated GitHub API (60 req/hr)")
    
    def scrape(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search all GitHub issues
        
        Args:
            query: Search term (e.g., "langchain bug", "n8n error")
            limit: Max results
        """
        print(f"🔍 Searching GitHub Issues for: '{query}'")
        
        url = f"{self.BASE_URL}/search/issues"
        params = {
            "q": f"{query} type:issue",
            "sort": "reactions",  # Most reacted = most painful
            "order": "desc",
            "per_page": min(limit, 100)
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for issue in data.get("items", []):
                results.append({
                    "type": "issue",
                    "id": str(issue.get("id")),
                    "number": issue.get("number"),
                    "title": issue.get("title"),
                    "text": issue.get("title") + " " + (issue.get("body") or "")[:500],
                    "url": issue.get("html_url"),
                    "repo": issue.get("repository_url", "").split("/")[-2:],
                    "state": issue.get("state"),
                    "author": issue.get("user", {}).get("login"),
                    "reactions": issue.get("reactions", {}).get("total_count", 0),
                    "comments": issue.get("comments", 0),
                    "labels": [l.get("name") for l in issue.get("labels", [])],
                    "created_at": issue.get("created_at"),
                    "source": "github"
                })
            
            self.results = results
            print(f"📊 Found {len(results)} issues")
            return results
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print("❌ Rate limited! Wait an hour or add a GitHub token.")
            else:
                print(f"❌ GitHub API error: {e}")
            return []
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def scrape_repo_issues(self, owner: str, repo: str, 
                           labels: List[str] = None,
                           state: str = "open",
                           limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get issues from a specific repository
        
        Args:
            owner: Repo owner (e.g., "langchain-ai")
            repo: Repo name (e.g., "langchain")
            labels: Filter by labels (e.g., ["bug", "help wanted"])
            state: "open", "closed", or "all"
            limit: Max results
        """
        print(f"🔍 Getting issues from {owner}/{repo}")
        
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/issues"
        params = {
            "state": state,
            "sort": "reactions",
            "direction": "desc",
            "per_page": min(limit, 100)
        }
        
        if labels:
            params["labels"] = ",".join(labels)
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            response.raise_for_status()
            issues = response.json()
            
            results = []
            for issue in issues:
                # Skip pull requests (they also come through issues endpoint)
                if "pull_request" in issue:
                    continue
                    
                results.append({
                    "type": "issue",
                    "id": str(issue.get("id")),
                    "number": issue.get("number"),
                    "title": issue.get("title"),
                    "text": issue.get("title") + " " + (issue.get("body") or "")[:500],
                    "url": issue.get("html_url"),
                    "repo": f"{owner}/{repo}",
                    "state": issue.get("state"),
                    "author": issue.get("user", {}).get("login"),
                    "reactions": issue.get("reactions", {}).get("total_count", 0),
                    "comments": issue.get("comments", 0),
                    "labels": [l.get("name") for l in issue.get("labels", [])],
                    "created_at": issue.get("created_at"),
                    "source": "github"
                })
            
            self.results = results
            print(f"📊 Found {len(results)} issues in {owner}/{repo}")
            return results
            
        except Exception as e:
            print(f"❌ Error fetching repo issues: {e}")
            return []
    
    def find_painful_issues(self, owner: str, repo: str, 
                            min_reactions: int = 5) -> List[Dict[str, Any]]:
        """
        Find issues with high engagement (= painful problems)
        
        High reactions + many comments = real pain point
        """
        issues = self.scrape_repo_issues(owner, repo, limit=100)
        
        painful = [
            issue for issue in issues
            if issue.get("reactions", 0) >= min_reactions
            or issue.get("comments", 0) >= 10
        ]
        
        # Sort by total engagement
        painful.sort(key=lambda x: x.get("reactions", 0) + x.get("comments", 0), reverse=True)
        
        print(f"🎯 Found {len(painful)} high-engagement issues")
        return painful


# Quick test
if __name__ == "__main__":
    scraper = GitHubIssuesScraper()  # No token = 60 req/hr
    
    # Test 1: Search all issues
    results = scraper.scrape("langchain error", limit=10)
    
    for r in results[:3]:
        print(f"\n📌 [{r['state']}] {r['title'][:50]}...")
        print(f"   Reactions: {r['reactions']} | Comments: {r['comments']}")
        print(f"   Labels: {r['labels'][:3]}")
    
    # Test 2: Get painful issues from a specific repo
    # painful = scraper.find_painful_issues("langchain-ai", "langchain", min_reactions=10)
    
    scraper.save_results()

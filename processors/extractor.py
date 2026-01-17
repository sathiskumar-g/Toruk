"""
Problem Extractor
Extracts and categorizes problems from scraped data
"""
import re
from typing import List, Dict, Any
from datetime import datetime
import json
import os

# Import from config
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PROBLEM_KEYWORDS, CATEGORIES


class ProblemExtractor:
    """
    Extract problems from raw scraped data
    
    Takes raw posts/issues and:
    1. Filters for problem-related content
    2. Extracts the core problem statement
    3. Categorizes the problem
    4. Identifies the affected tool/platform
    """
    
    def __init__(self):
        self.keywords = PROBLEM_KEYWORDS
        self.categories = CATEGORIES
        self.problems: List[Dict[str, Any]] = []
        
    def extract_problems(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process raw scraped items and extract problems
        
        Args:
            items: Raw scraped data from any source
            
        Returns:
            List of structured problem objects
        """
        print(f"🔬 Extracting problems from {len(items)} items...")
        
        problems = []
        for item in items:
            problem = self._process_item(item)
            if problem:
                problems.append(problem)
        
        self.problems = problems
        print(f"✅ Extracted {len(problems)} problems")
        return problems
    
    def _process_item(self, item: Dict[str, Any]) -> Dict[str, Any] | None:
        """Process a single item and extract problem if valid"""
        
        text = item.get("text", "")
        title = item.get("title", "")
        full_text = f"{title} {text}".lower()
        
        # Check if it contains problem keywords
        matched_keywords = [kw for kw in self.keywords if kw.lower() in full_text]
        
        if not matched_keywords:
            return None
        
        # Calculate pain intensity based on language
        pain_score = self._calculate_pain_score(full_text, matched_keywords)
        
        # Extract the core problem statement
        problem_statement = self._extract_problem_statement(title, text)
        
        # Categorize the problem
        category = self._categorize(full_text)
        
        # Identify tools mentioned
        tools_mentioned = self._extract_tools(full_text)
        
        return {
            "id": item.get("id"),
            "source": item.get("source"),
            "type": item.get("type"),
            "url": item.get("url"),
            "original_title": title,
            "problem_statement": problem_statement,
            "full_text": text if text else title,  # Store complete full text for UI
            "category": category,
            "tools_mentioned": tools_mentioned,
            "matched_keywords": matched_keywords,
            "pain_score": pain_score,
            "engagement": {
                "reactions": item.get("reactions", item.get("points", 0)),
                "comments": item.get("comments", 0)
            },
            "author": item.get("author"),
            "created_at": item.get("created_at"),
            "extracted_at": datetime.now().isoformat()
        }
    
    def _calculate_pain_score(self, text: str, matched_keywords: List[str]) -> int:
        """
        Calculate pain intensity (1-10)
        
        High pain indicators:
        - Multiple problem keywords
        - Strong emotional language
        - Urgency words
        - "give up" / "switched to"
        """
        score = min(len(matched_keywords) * 2, 6)  # Base score from keywords
        
        # High pain phrases
        high_pain_phrases = [
            "gave up", "give up", "switched to", "moved away",
            "waste of time", "hours trying", "days trying",
            "completely broken", "unusable", "nightmare",
            "worst experience", "so frustrated"
        ]
        
        for phrase in high_pain_phrases:
            if phrase in text:
                score += 2
        
        # Urgency indicators
        if "urgent" in text or "asap" in text or "blocking" in text:
            score += 1
        
        return min(score, 10)
    
    def _extract_problem_statement(self, title: str, text: str) -> str:
        """Extract a clean problem statement"""
        
        # Avoid titles that are solutions ("I built", "Here's how", "My AI")
        solution_indicators = ["i built", "i created", "here's how", "my ai", "i made", "tutorial", "guide"]
        title_lower = title.lower()
        
        is_solution_post = any(indicator in title_lower for indicator in solution_indicators)
        
        # If title describes a problem clearly, use it
        problem_indicators = ["error", "issue", "problem", "bug", "fail", "broken", "can't", "won't", "doesn't work"]
        if not is_solution_post and len(title) > 20 and any(kw in title_lower for kw in problem_indicators):
            return title
        
        # Otherwise, extract from text - look for problem sentences
        sentences = re.split(r'[.!?]', text)
        
        for sentence in sentences[:8]:  # First 8 sentences
            sentence = sentence.strip()
            sentence_lower = sentence.lower()
            
            # Skip solution sentences
            if any(indicator in sentence_lower for indicator in solution_indicators):
                continue
            
            # Look for problem keywords
            if len(sentence) > 30 and any(kw in sentence_lower for kw in self.keywords[:15]):
                return sentence[:250]
        
        # Fallback to first substantial text
        if text and len(text) > 50:
            return text[:200]
        
        # Last resort: use title
        return title
    
    def _categorize(self, text: str) -> str:
        """Categorize the problem"""
        
        category_keywords = {
            "API Integration": ["api", "endpoint", "rest", "graphql", "webhook"],
            "Authentication": ["auth", "login", "token", "oauth", "permission"],
            "Documentation": ["docs", "documentation", "example", "tutorial"],
            "Performance": ["slow", "performance", "memory", "timeout", "latency"],
            "Error Handling": ["error", "exception", "crash", "traceback"],
            "Configuration": ["config", "setup", "install", "environment"],
            "Data/State": ["data", "state", "storage", "database", "sync"],
            "UX/Workflow": ["workflow", "confusing", "complicated", "ux"],
            "Cost/Pricing": ["cost", "expensive", "pricing", "credits", "tokens"],
            "Compatibility": ["version", "compatible", "update", "breaking"]
        }
        
        for category, keywords in category_keywords.items():
            if any(kw in text for kw in keywords):
                return category
        
        return "General"
    
    def _extract_tools(self, text: str) -> List[str]:
        """Extract tool names mentioned in the text"""
        
        known_tools = [
            "langchain", "langgraph", "openai", "gpt", "claude", "anthropic",
            "n8n", "zapier", "make", "flowise", "dify", "autogen",
            "pinecone", "weaviate", "chromadb", "qdrant", "supabase",
            "vercel", "netlify", "railway", "docker", "kubernetes"
        ]
        
        mentioned = [tool for tool in known_tools if tool in text]
        return mentioned
    
    def save_problems(self, filename: str = None) -> str:
        """Save extracted problems to JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/problems_{timestamp}.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        output = {
            "extracted_at": datetime.now().isoformat(),
            "count": len(self.problems),
            "problems": self.problems
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved {len(self.problems)} problems to {filename}")
        return filename
    
    def get_top_problems(self, n: int = 10) -> List[Dict[str, Any]]:
        """Get top N problems by pain score and engagement"""
        
        sorted_problems = sorted(
            self.problems,
            key=lambda x: (
                x.get("pain_score", 0) * 10 +
                x.get("engagement", {}).get("reactions", 0) +
                x.get("engagement", {}).get("comments", 0)
            ),
            reverse=True
        )
        
        return sorted_problems[:n]


# Test
if __name__ == "__main__":
    # Test with sample data
    sample_items = [
        {
            "id": "1",
            "source": "hackernews",
            "type": "comment",
            "title": "LangChain is overly complicated",
            "text": "I spent 3 days trying to get a simple RAG pipeline working with LangChain. The documentation is terrible and error messages are useless. Finally gave up and wrote it myself in 100 lines.",
            "url": "https://example.com",
            "points": 45,
            "comments": 12,
            "author": "dev123"
        },
        {
            "id": "2",
            "source": "github",
            "type": "issue",
            "title": "Memory leak when using streaming with GPT-4",
            "text": "After running for about 2 hours with streaming enabled, memory usage grows to 10GB and the app crashes. This is a critical bug for production use.",
            "url": "https://github.com/example/issue/123",
            "reactions": 28,
            "comments": 15,
            "author": "produser"
        }
    ]
    
    extractor = ProblemExtractor()
    problems = extractor.extract_problems(sample_items)
    
    for p in problems:
        print(f"\n🎯 Problem: {p['problem_statement'][:60]}...")
        print(f"   Category: {p['category']} | Pain: {p['pain_score']}/10")
        print(f"   Tools: {p['tools_mentioned']}")

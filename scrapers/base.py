"""
Base Scraper Class
All scrapers inherit from this to ensure consistent interface
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime
import json
import os


class BaseScraper(ABC):
    """Base class for all scrapers"""
    
    def __init__(self, name: str):
        self.name = name
        self.results: List[Dict[str, Any]] = []
        
    @abstractmethod
    def scrape(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Main scrape method - must be implemented by subclasses
        
        Args:
            query: Search term or topic to scrape
            limit: Maximum number of results
            
        Returns:
            List of problem dictionaries
        """
        pass
    
    def save_results(self, filename: str = None) -> str:
        """Save scraped results to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/{self.name}_{timestamp}.json"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        output = {
            "source": self.name,
            "scraped_at": datetime.now().isoformat(),
            "count": len(self.results),
            "results": self.results
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {len(self.results)} results to {filename}")
        return filename
    
    def filter_by_keywords(self, items: List[Dict], keywords: List[str], text_field: str = "text") -> List[Dict]:
        """Filter items that contain any of the problem keywords"""
        filtered = []
        for item in items:
            text = item.get(text_field, "").lower()
            if any(kw.lower() in text for kw in keywords):
                # Mark which keywords matched
                matched = [kw for kw in keywords if kw.lower() in text]
                item["matched_keywords"] = matched
                filtered.append(item)
        return filtered

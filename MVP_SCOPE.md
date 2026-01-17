# 🎯 MVP SCOPE: Problem Research Tool

## Version 1.0 - Simple Scraper + AI Analyzer

**Timeline:** 1 Week  
**Goal:** Collect and analyze 100 problems from free sources  
**No paid APIs needed**

---

## 📋 MVP FEATURES

### What We're Building

| Feature | Priority | Effort |
|---------|----------|--------|
| Hacker News scraper | P0 | 2 hours |
| GitHub Issues scraper | P0 | 2 hours |
| Manual content analyzer | P0 | 1 hour |
| JSON storage | P0 | 1 hour |
| Simple CLI interface | P1 | 2 hours |
| Problem scoring | P1 | 2 hours |

### What We're NOT Building (Yet)

- ❌ Reddit API integration (too expensive)
- ❌ Web UI / Dashboard
- ❌ Automated scheduling
- ❌ Database (PostgreSQL)
- ❌ User accounts

---

## 🛠️ TECHNICAL SCOPE

### Data Sources (Free Only)

| Source | Method | Rate Limit |
|--------|--------|------------|
| **Hacker News** | Official API | None |
| **GitHub** | REST API (unauthenticated) | 60/hour |
| **Product Hunt** | GraphQL API | Limited |
| **Manual paste** | User provides content | None |

### Tech Stack

```
Python 3.11+
├── requests        # HTTP calls
├── beautifulsoup4  # HTML parsing (backup)
├── json            # Data storage
└── (optional) anthropic/openai  # AI analysis
```

### File Outputs

```
data/
├── hackernews_posts.json      # Raw HN data
├── github_issues.json         # Raw GitHub issues
├── extracted_problems.json    # Processed problems
└── opportunities.json         # Scored opportunities
```

---

## 📊 DATA MODELS

### Raw Post (from any source)

```python
{
    "id": "hn_12345",
    "source": "hackernews",
    "url": "https://news.ycombinator.com/item?id=12345",
    "title": "Post title",
    "content": "Full text content",
    "author": "username",
    "date": "2026-01-17",
    "score": 150,
    "comments": 45,
    "tags": ["AI", "LangChain"]
}
```

### Extracted Problem

```python
{
    "id": "prob_001",
    "source_id": "hn_12345",
    "source_url": "...",
    "tool_mentioned": "LangChain",
    "direct_quote": "Exact user words",
    "problem_summary": "One line summary",
    "category": "debugging",
    "severity": 4,
    "user_type": "developer",
    "extracted_at": "2026-01-17T10:00:00Z"
}
```

### Scored Opportunity

```python
{
    "problem_id": "prob_001",
    "scores": {
        "pain": 8,
        "market": 7,
        "monetization": 6,
        "feasibility": 8,
        "saturation": 3
    },
    "total_score": 7.4,
    "recommendation": "BUILD",
    "suggested_solution": "Debugging tool for LangChain",
    "effort_estimate": "1 month",
    "revenue_model": "subscription"
}
```

---

## 🔍 SEARCH KEYWORDS (Hardcoded in MVP)

### Tools to Monitor

```python
TOOLS = [
    "langchain", "n8n", "zapier", "make", 
    "openai", "chatgpt", "claude", "cursor",
    "copilot", "vercel", "supabase"
]
```

### Problem Keywords

```python
PROBLEM_KEYWORDS = [
    "frustrated", "annoying", "broken", "fails",
    "doesn't work", "bug", "error", "problem",
    "limitation", "missing", "expensive", "slow",
    "confusing", "terrible", "hate", "wish"
]
```

### Categories

```python
CATEGORIES = [
    "debugging", "cost", "reliability", "integration",
    "memory", "performance", "documentation", "security"
]
```

---

## 🚀 MVP WORKFLOW

### Step 1: Collect Data

```bash
python run.py collect --source hackernews --query "langchain problem"
python run.py collect --source github --repo "langchain-ai/langchain"
```

### Step 2: Extract Problems

```bash
python run.py extract --input data/hackernews_posts.json
# OR
python run.py extract --text "paste content here"
```

### Step 3: Score Opportunities

```bash
python run.py score --input data/extracted_problems.json
```

### Step 4: View Results

```bash
python run.py report --top 10
```

---

## 📁 MVP FILE STRUCTURE

```
torukmacto/
├── MASTER_PROBLEM_RESEARCH.md
├── MVP_SCOPE.md
├── requirements.txt
├── run.py                    # CLI entry point
├── config.py                 # Keywords, tools list
├── scrapers/
│   ├── __init__.py
│   ├── base.py               # Base scraper class
│   ├── hackernews.py         # HN API
│   └── github_issues.py      # GitHub API
├── processors/
│   ├── __init__.py
│   ├── extractor.py          # Problem extraction
│   └── scorer.py             # Opportunity scoring
├── data/                     # Output directory
│   └── .gitkeep
└── prompts/
    └── extraction.txt        # AI prompts
```

---

## ✅ ACCEPTANCE CRITERIA

### MVP is complete when:

- [ ] Can fetch last 50 HN posts mentioning AI tools
- [ ] Can fetch open issues from 3 repos
- [ ] Can extract problems from pasted text
- [ ] Saves structured JSON output
- [ ] Basic scoring formula works
- [ ] CLI is functional

### Success = Finding 10 real problems worth exploring

---

## ⏱️ TIMELINE

| Day | Task |
|-----|------|
| 1 | Setup + HN scraper |
| 2 | GitHub scraper |
| 3 | Problem extractor |
| 4 | Scoring system |
| 5 | CLI + polish |
| 6 | Run + collect 100 problems |
| 7 | Review + pick top 5 |

---

## 🔮 FUTURE VERSIONS

### v1.1 (Week 2)
- Add Google search scraping
- Better AI prompts
- Export to CSV/Notion

### v1.2 (Week 3)
- Scheduled runs (cron)
- Trend detection
- Email digest

### v2.0 (Month 2)
- Web dashboard
- Database storage
- Team sharing

---

## 💡 KEY PRINCIPLES

1. **Start small** - 2 sources is enough for MVP
2. **JSON first** - No database until needed
3. **CLI is fine** - No UI until validated
4. **Manual is OK** - Semi-automation beats over-engineering
5. **Ship fast** - Perfect is the enemy of done

---

*"The goal is not a perfect tool. The goal is finding problems worth solving."*

# 🦅 TORUKMACTO - Complete Project Documentation

**Automated Reddit Research Engine for Finding Micro SaaS Opportunities**

---

## 📚 Table of Contents

1. [Project Overview](#-project-overview)
2. [How It Works](#-how-it-works)
3. [Installation & Setup](#-installation--setup)
4. [CLI Usage](#-cli-usage)
5. [Web UI Usage](#-web-ui-usage)
6. [Project Architecture](#-project-architecture)
7. [File Structure](#-file-structure)
8. [Scoring System](#-scoring-system)
9. [Rate Limiting & API](#-rate-limiting--api)
10. [Customization](#-customization)
11. [Troubleshooting](#-troubleshooting)

---

## 🎯 Project Overview

### What is TORUKMACTO?

TORUKMACTO is an **automated problem discovery engine** that scrapes Reddit to find real, painful, monetizable problems in the AI tools and automation ecosystem. It helps you discover Micro SaaS opportunities by analyzing actual user complaints and pain points.

### Key Features

- ✅ **Free Reddit JSON API** - No authentication required
- ✅ **Custom Keyword Research** - Search with your own problem keywords
- ✅ **Batch Processing** - Process multiple keywords in one run
- ✅ **5P Scoring Framework** - Scores opportunities on Pain, Pervasiveness, Proximity, Payment, Plausibility
- ✅ **Web UI** - Beautiful terminal-themed interface for viewing results
- ✅ **Rate Limit Management** - Built-in delays and error handling
- ✅ **Aggregate Reports** - Combines all results and ranks top opportunities

### What You Get

**1. Terminal Output:**
```
[1/6] Processing: n8n workflow breaks
🔍 Searching ALL of Reddit for: 'n8n workflow breaks'
   Found 5 posts (total: 5)
✅ Returned 5 unique results for 'n8n workflow breaks'
🔬 Extracting problems from 5 items...
✅ Extracted 2 problems
📊 Scoring 2 problems...
✅ Scored and ranked 2 opportunities
✅ Completed n8n workflow breaks: 2 opportunities
```

**2. JSON Files:**
- Individual keyword results: `data/reddit_<keyword>_*.json`
- Final aggregate report: `data/reddit_research_final_*.json`

**3. Web UI Dashboard:**
- Summary cards (keywords processed, opportunities found, top score)
- Keyword summary table with status indicators
- Opportunity cards with full post content (scrollable 200px height)
- Tabs: Top 10 / All opportunities
- Score breakdown (Pain, Pervasiveness, Proximity, Payment, Plausibility)
- Recommendation badges (💰 WORTH, 🔥 HIGH, ✅ GOOD, ⚠️ MODERATE, ❌ LOW)

---

## 🔧 How It Works

### End-to-End Flow

```
┌──────────────────────────────────────────────────────────────┐
│  1. USER CREATES KEYWORDS                                    │
│     research_keywords.json                                   │
│     ["n8n workflow breaks", "Zapier rate limit problem"]     │
└───────────────────────┬──────────────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────────────┐
│  2. CLI COMMAND                                              │
│     python run.py batch-reddit --limit 5                     │
│     OR                                                       │
│     python api.py (Web UI)                                   │
└───────────────────────┬──────────────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────────────┐
│  3. REDDIT SCRAPER (scrapers/reddit.py)                      │
│     - Uses free Reddit JSON API                              │
│     - Searches ALL of Reddit (not specific subreddits)       │
│     - Applies rate limiting (3 sec delays)                   │
│     - Handles 429 errors (10 sec wait)                       │
│     - Returns: title, full_text, url, author, points, etc.   │
└───────────────────────┬──────────────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────────────┐
│  4. PROBLEM EXTRACTOR (processors/extractor.py)              │
│     - Filters posts with problem keywords                    │
│     - Avoids solution posts ("I built", "My AI")             │
│     - Extracts problem statements                            │
│     - Categorizes (Documentation, API, Performance, etc.)    │
│     - Detects tools mentioned (n8n, Zapier, Make, etc.)      │
│     - Calculates initial pain score                          │
│     - Stores FULL post text (no truncation)                  │
└───────────────────────┬──────────────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────────────┐
│  5. OPPORTUNITY SCORER (processors/scorer.py)                │
│     - Scores on 5 dimensions:                                │
│       • Pain: 0-10 (engagement + keywords)                   │
│       • Pervasiveness: 0-10 (engagement thresholds)          │
│       • Proximity: 0-10 (subreddit relevance)                │
│       • Payment: 0-10 (payment intent keywords)              │
│       • Plausibility: 0-10 (technical feasibility)           │
│     - Calculates total score (sum of all 5)                  │
│     - Generates recommendation:                              │
│       • 35+ = 💰 WORTH OPPORTUNITY                           │
│       • 30+ = 🔥 HIGH OPPORTUNITY                            │
│       • 25+ = ✅ GOOD OPPORTUNITY                            │
│       • 20+ = ⚠️ MODERATE                                    │
│       • <20 = ❌ LOW PRIORITY                                │
└───────────────────────┬──────────────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────────────┐
│  6. RESULTS AGGREGATOR (run.py)                              │
│     - Combines all keyword results                           │
│     - Ranks all opportunities by total score                 │
│     - Assigns rank numbers (#1, #2, #3...)                   │
│     - Saves final report: reddit_research_final_*.json       │
└───────────────────────┬──────────────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────────────┐
│  7. OUTPUT                                                   │
│     A. Terminal: Progress logs + summary                     │
│     B. JSON Files: Full structured data                      │
│     C. Web UI: Interactive dashboard                         │
└──────────────────────────────────────────────────────────────┘
```

### Key Components

**1. Reddit Scraper (`scrapers/reddit.py`)**
- Uses Reddit's free JSON API: `https://www.reddit.com/search.json?q=query`
- No authentication required
- Rate limiting: 3 second delays between requests
- 429 error handling: 10 second wait + continue
- Returns full post text (no truncation)

**2. Problem Extractor (`processors/extractor.py`)**
- Filters posts with problem keywords: "error", "issue", "problem", "bug", "fail", etc.
- Avoids solution posts: "I built", "My AI", "Here's how"
- Extracts clean problem statements (avoids titles that are solutions)
- Categorizes into: Documentation, API Integration, Performance, Data Privacy, Configuration, General
- Detects 40+ tools: langchain, n8n, zapier, make, openai, claude, etc.
- Stores complete post text in `full_text` field

**3. Opportunity Scorer (`processors/scorer.py`)**
- **Pain Score (0-10)**: Based on engagement metrics and pain keywords
  - Keywords: "frustrated", "terrible", "hate", "impossible", etc.
  - High engagement (100+ upvotes) = higher pain
  
- **Pervasiveness Score (0-10)**: How widespread the problem is
  - 100+ upvotes = 10
  - 50-100 = 8
  - 20-50 = 6
  - 10-20 = 4
  - <10 = 2
  
- **Proximity Score (0-10)**: Target customer relevance
  - Tech subreddits (r/programming, r/webdev) = 10
  - AI subreddits (r/OpenAI, r/ChatGPT) = 8
  - Other = 5
  
- **Payment Potential (0-10)**: Likelihood they'll pay
  - Keywords: "willing to pay", "need a solution", "subscription"
  - Business context = higher score
  
- **Plausibility Score (0-10)**: Can you build it?
  - Requires specific tools mentioned = more feasible
  - Clear problem statement = easier to solve

**4. Web UI (`api.py` + `static/`)**
- Flask backend serving JSON API
- Terminal-themed interface (black/grey/white + green/orange/purple)
- Features:
  - Keyword management (add/remove)
  - Posts per keyword limiter
  - Real-time research progress
  - Summary cards and tables
  - Opportunity cards with:
    - Rank badge (#1, #2, etc.)
    - Original title (clickable link)
    - Problem statement
    - **Scrollable post content (200px fixed height)**
    - Meta info (author, upvotes, comments, category)
    - Score breakdown (all 5 dimensions)
    - Recommendation badge
  - Tabs: Top 10 / All opportunities
  - Export results as JSON

---

## 🚀 Installation & Setup

### Prerequisites

- **Python 3.8+** (tested on Python 3.12)
- **pip** (Python package manager)
- **Internet connection** (for Reddit API)

### Step 1: Install Dependencies

```powershell
# Navigate to project directory
cd s:\Engineering\2026\one\mock\torukmacto

# Install required packages
pip install -r requirements.txt
```

**Dependencies:**
- `requests` - HTTP requests to Reddit API
- `beautifulsoup4` - HTML/JSON parsing
- `flask` - Web server for UI
- `flask-cors` - CORS support for API

**Installation time:** ~10 seconds  
**Total size:** ~10 MB

### Step 2: Verify Installation

```powershell
# Test that everything works
python run.py demo
```

You should see:
```
🎯 TORUKMACTO Demo Mode
🔍 Searching Reddit for: 'langchain'
...
✅ Demo complete!
```

---

## 💻 CLI Usage

### Quick Commands

```powershell
# 1. Run demo (tests basic functionality)
python run.py demo

# 2. Batch research with custom keywords
python run.py batch-reddit --limit 5

# 3. Search specific topic
python run.py search "n8n workflow"

# 4. Full scan of all tools
python run.py scan --all

# 5. Convert JSON to table view
python json_to_table.py data/reddit_research_final_*.json
```

### Batch Reddit Research (Recommended)

**Step 1: Create/Edit Keywords**

```powershell
# Edit keywords file
notepad research_keywords.json
```

```json
{
  "reddit_keywords": [
    "n8n workflow breaks",
    "Zapier rate limit problem",
    "Make.com debugging issues",
    "webhook automation fails"
  ]
}
```

**Step 2: Run Batch Research**

```powershell
python run.py batch-reddit --limit 5
```

**What happens:**
1. Loads keywords from `research_keywords.json`
2. For each keyword:
   - Searches ALL of Reddit
   - Extracts problems
   - Scores opportunities
   - Saves individual results
3. Combines all results
4. Ranks top opportunities
5. Saves final report: `data/reddit_research_final_YYYYMMDD_HHMMSS.json`

**Options:**
- `--limit N` - Posts per keyword (default: 20)
- `--keywords-file PATH` - Custom keywords file path

**Example output:**
```
[1/4] Processing: n8n workflow breaks
🔍 Searching ALL of Reddit for: 'n8n workflow breaks'
   Found 5 posts (total: 5)
✅ Extracted 2 problems
✅ Scored and ranked 2 opportunities
✅ Completed n8n workflow breaks: 2 opportunities

[2/4] Processing: Zapier rate limit problem
...

✅ BATCH RESEARCH COMPLETE!
📊 Total: 4 keywords, 8 opportunities found
🏆 Top Score: 34.0
💾 Results saved to: data/reddit_research_final_20260117_172753.json
```

### View Results as Table

```powershell
python json_to_table.py data/reddit_research_final_20260117_172753.json
```

**Output:**
```
╔═══════════════════════════════════════════════════════════════╗
║                   REDDIT RESEARCH RESULTS                      ║
║                     Top 10 Opportunities                       ║
╚═══════════════════════════════════════════════════════════════╝

Rank #1 | Score: 34.0 | 💰 WORTH OPPORTUNITY
─────────────────────────────────────────────────────────────────
Title: My AI actually remembers my entire Home Assistant setup...
Problem: My AI actually remembers my entire Home Assistant setup...
Category: Documentation | Tools: claude, make
Engagement: ⬆️ 156 | 💬 91
URL: https://www.reddit.com/r/homeassistant/comments/1m2qkjn/...
─────────────────────────────────────────────────────────────────
```

---

## 🌐 Web UI Usage

### Starting the Web Server

```powershell
# Navigate to project
cd s:\Engineering\2026\one\mock\torukmacto

# Start Flask server
python api.py
```

**Output:**
```
🚀 Starting TORUKMACTO Research API...
📡 Open http://localhost:5000 in your browser
 * Running on http://127.0.0.1:5000
```

### Using the Web Interface

**1. Open Browser**
```
http://localhost:5000
```

**2. Add Keywords**
- Type keyword in input box
- Press Enter or click "Add Keyword"
- Keywords appear as green tags
- Click ❌ to remove

**3. Set Posts Limit**
- Default: 20 posts per keyword
- Adjust slider: 5-100 posts
- Lower = faster, Higher = more comprehensive

**4. Start Research**
- Click green "Start Research" button
- Progress shows in logs (Processing 1/6...)
- Summary appears when complete

**5. View Results**

**Summary Cards:**
- Keywords Processed
- Opportunities Found
- Top Score

**Keyword Summary Table:**
- Keyword name
- Posts scraped
- Problems found
- Opportunities scored
- Top score
- Status (✅ Success / ⚠️ Error / ⚪ No results)

**Opportunity Cards:**
- **Rank badge** (#1, #2, #3...)
- **Title** (green link to original Reddit post)
- **Keyword tag** (🔑 which keyword found it)
- **Problem statement** (extracted core problem)
- **📄 Post Content** (NEW!)
  - Scrollable box with full text
  - Fixed 200px height
  - Terminal-themed scrollbar
  - Read complete post without leaving UI
- **Meta info** (👤 author, ⬆️ upvotes, 💬 comments, 📂 category)
- **Score breakdown** (Pain, Pervasiveness, Proximity, Payment, Plausibility)
- **Recommendation badge**
  - 💰 WORTH OPPORTUNITY (35+) - Orange background
  - 🔥 HIGH OPPORTUNITY (30+) - Red background
  - ✅ GOOD OPPORTUNITY (25+) - Green background
  - ⚠️ MODERATE (20+) - Yellow background
  - ❌ LOW PRIORITY (<20) - Grey background

**6. Switch Views**
- **Top 10** - Best opportunities only
- **All (N)** - Complete list

**7. Export Results**
- Click "Export Results" button
- Downloads: `reddit_research_YYYY-MM-DD.json`

### Web UI Features

**Terminal Theme:**
- Background: Black (#0a0a0a)
- Panels: Dark grey (#1a1a1a)
- Borders: Grey (#333)
- Text: White (#ffffff)
- Primary action: Green (#00ff00) with glow effect
- Destructive: Orange (#ff6b00)
- Scores: Purple (#9900ff)
- System font (not monospace)

**Scrollable Post Content:**
- Full post text preserved (no truncation)
- 200px fixed height container
- Auto scroll on overflow
- Styled scrollbar:
  - Track: Dark grey (#1a1a1a)
  - Thumb: Grey (#333)
  - Hover: Light grey (#555)

**Error Handling:**
- Red status icons (⚠️) for failed keywords
- Error messages displayed in keyword table
- Research continues on error (doesn't stop)

---

## 🏗️ Project Architecture

### Directory Structure

```
torukmacto/
├── README.md                          # Original project documentation
├── readme_torukmacto.md              # THIS FILE - Complete guide
├── requirements.txt                  # Python dependencies
├── config.py                         # Configuration (tools, keywords, repos)
├── run.py                            # Main CLI entry point
├── api.py                            # Flask web server
├── json_to_table.py                  # JSON to table converter
├── research_keywords.json            # Custom keyword list
│
├── scrapers/                         # Data collection
│   ├── __init__.py
│   ├── base.py                       # Base scraper class
│   ├── reddit.py                     # Reddit JSON API scraper
│   ├── hackernews.py                 # HackerNews Algolia API
│   └── github_issues.py              # GitHub Issues API
│
├── processors/                       # Data processing
│   ├── __init__.py
│   ├── extractor.py                  # Problem extraction & categorization
│   └── scorer.py                     # 5P opportunity scoring
│
├── static/                           # Web UI files
│   ├── index.html                    # Main UI page
│   ├── styles.css                    # Terminal theme CSS
│   └── app.js                        # Frontend JavaScript
│
└── data/                             # Results (gitignored)
    ├── reddit_<keyword>_*.json       # Individual keyword results
    ├── reddit_research_final_*.json  # Aggregate reports
    ├── search_*.json                 # Search results
    └── full_scan_*.json              # Full scan results
```

### Code Architecture

**Layer 1: Scraper (Data Collection)**
```python
# scrapers/reddit.py
class RedditScraper:
    def scrape(query, limit):
        # 1. Build search URL
        # 2. Apply rate limiting
        # 3. Make HTTP request
        # 4. Parse JSON response
        # 5. Return list of posts
```

**Layer 2: Extractor (Problem Extraction)**
```python
# processors/extractor.py
class ProblemExtractor:
    def extract_problems(posts):
        # 1. Filter posts with problem keywords
        # 2. Avoid solution posts
        # 3. Extract problem statement
        # 4. Categorize problem type
        # 5. Detect tools mentioned
        # 6. Calculate pain score
        # 7. Return structured problems
```

**Layer 3: Scorer (Opportunity Scoring)**
```python
# processors/scorer.py
class OpportunityScorer:
    def score_opportunities(problems):
        # 1. Score pain (0-10)
        # 2. Score pervasiveness (0-10)
        # 3. Score proximity (0-10)
        # 4. Score payment potential (0-10)
        # 5. Score plausibility (0-10)
        # 6. Calculate total score
        # 7. Generate recommendation
        # 8. Rank by total score
```

**Layer 4: API (Web Interface)**
```python
# api.py
@app.route('/api/research', methods=['POST'])
def run_research():
    # 1. Load keywords from request
    # 2. For each keyword:
    #    - Scrape Reddit
    #    - Extract problems
    #    - Score opportunities
    # 3. Aggregate results
    # 4. Return JSON response
```

---

## 📊 Scoring System

### 5P Framework (5 Dimensions × 10 Points = 50 Total)

**1. Pain Score (0-10)**
- **What it measures:** How much the problem hurts
- **Calculation:**
  - Base: 5 points
  - Pain keywords (+1 each): "frustrated", "terrible", "hate", "impossible", "waste of time", etc.
  - High engagement (+2 if 50+ upvotes)
  - Max: 10 points

**2. Pervasiveness Score (0-10)**
- **What it measures:** How many people have this problem
- **Calculation:**
  - 100+ upvotes = 10
  - 50-100 upvotes = 8
  - 20-50 upvotes = 6
  - 10-20 upvotes = 4
  - <10 upvotes = 2

**3. Proximity Score (0-10)**
- **What it measures:** Are they your target customers?
- **Calculation:**
  - Tech subreddits (r/programming, r/webdev, r/Python) = 10
  - AI subreddits (r/OpenAI, r/ChatGPT, r/LocalLLaMA) = 8
  - Other subreddits = 5

**4. Payment Potential Score (0-10)**
- **What it measures:** Will they pay to solve it?
- **Calculation:**
  - Base: 5 points
  - Payment keywords (+2 each): "willing to pay", "need a solution", "subscription", "paid", "buy"
  - Business context (+2): "company", "team", "enterprise"
  - Max: 10 points

**5. Plausibility Score (0-10)**
- **What it measures:** Can you realistically build a solution?
- **Calculation:**
  - Tools mentioned (+2 per tool, max 4)
  - Clear problem statement (+3)
  - Base: 3 points
  - Max: 10 points (capped)

### Recommendation Thresholds

| Total Score | Recommendation | Badge | Action |
|------------|----------------|-------|--------|
| **35+** | 💰 WORTH OPPORTUNITY | Orange | **Build immediately** |
| **30-34** | 🔥 HIGH OPPORTUNITY | Red | **Worth pursuing immediately** |
| **25-29** | ✅ GOOD OPPORTUNITY | Green | **Worth exploring further** |
| **20-24** | ⚠️ MODERATE | Yellow | **Needs validation** |
| **<20** | ❌ LOW PRIORITY | Grey | **Skip for now** |

### Example Score Breakdown

```json
{
  "opportunity_score": {
    "pain": 8,              // High pain keywords + engagement
    "pervasiveness": 10,    // 156 upvotes
    "proximity": 6,         // r/homeassistant (niche but tech)
    "payment": 5,           // No explicit payment intent
    "plausibility": 9,      // Clear problem + tools mentioned
    "total": 38.0           // 💰 WORTH OPPORTUNITY
  }
}
```

---

## ⚡ Rate Limiting & API

### Reddit JSON API

**Endpoint:**
```
https://www.reddit.com/search.json?q=query&limit=100&raw_json=1
```

**Authentication:** None required (FREE!)

**Rate Limits:**
- No official documented limit
- Respectful self-imposed: 3 seconds between requests
- 429 handling: 10 second wait + continue

**Rate Limiting Implementation:**

```python
# In scrapers/reddit.py
self.request_delay = 3  # seconds
self.last_request_time = 0

# Before each request
elapsed = time.time() - self.last_request_time
if elapsed < self.request_delay:
    time.sleep(self.request_delay - elapsed)

# 429 error handling
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 429:
        print("⚠️ Rate limited. Waiting 10 seconds...")
        time.sleep(10)
```

**Pagination:**
- Reddit returns max 100 posts per page
- Use `after` parameter for next page
- Automatically handled in scraper

**Data Returned:**
- `id` - Unique post ID
- `title` - Post title
- `selftext` - Full post text (untruncated)
- `permalink` - URL to post
- `subreddit` - Subreddit name
- `author` - Username
- `score` - Upvotes (points)
- `num_comments` - Comment count
- `created_utc` - Timestamp

---

## 🎨 Customization

### 1. Add/Remove Keywords

**Edit `research_keywords.json`:**
```json
{
  "reddit_keywords": [
    "your new keyword",
    "another problem area",
    "specific tool issue"
  ]
}
```

**Tips:**
- Use specific problem phrases: "n8n webhook fails" (not just "n8n")
- Include error types: "Zapier rate limit", "API timeout"
- Mix tools + problems: "Make.com debugging", "webhook automation"

### 2. Customize Problem Keywords

**Edit `processors/extractor.py`:**
```python
# Line ~30
self.keywords = [
    # Problem indicators
    "error", "issue", "problem", "bug", "fail",
    # Emotions
    "frustrated", "annoying", "terrible", "hate",
    # Add your own
    "stuck", "confused", "broken", "doesn't work"
]
```

### 3. Add New Tool Detections

**Edit `processors/extractor.py`:**
```python
# Line ~60
tool_patterns = [
    r'\blangchain\b', r'\bn8n\b', r'\bzapier\b',
    # Add new tools
    r'\byour_tool\b', r'\banother_tool\b'
]
```

### 4. Adjust Scoring Weights

**Edit `processors/scorer.py`:**
```python
# Modify scoring logic
def _calculate_pain_score(self, problem: dict) -> int:
    score = 5  # Change base score
    # Adjust pain keyword weights
    pain_keywords = ["hate", "terrible"]  # Focus on strong emotions
    score += sum(2 for kw in pain_keywords if kw in text)  # +2 per keyword
    return min(score, 10)
```

### 5. Change Recommendation Thresholds

**Edit `processors/scorer.py`:**
```python
# Line ~150
if score >= 40:  # Change from 35
    return "💰 WORTH OPPORTUNITY - Build immediately"
elif score >= 35:  # Change from 30
    return "🔥 HIGH OPPORTUNITY - Worth pursuing immediately"
```

### 6. Customize Web UI Theme

**Edit `static/styles.css`:**
```css
/* Change color scheme */
:root {
    --bg-primary: #0a0a0a;      /* Background */
    --bg-secondary: #1a1a1a;    /* Panels */
    --text-primary: #ffffff;     /* Text */
    --accent-green: #00ff00;     /* Actions */
    --accent-orange: #ff6b00;    /* Destructive */
    --accent-purple: #9900ff;    /* Scores */
}
```

### 7. Adjust Posts Per Keyword

**In CLI:**
```powershell
python run.py batch-reddit --limit 50  # More posts per keyword
```

**In Web UI:**
- Use slider: 5-100 posts
- Default: 20 posts

---

## 🔧 Troubleshooting

### Common Issues

**1. ModuleNotFoundError: No module named 'flask'**
```powershell
# Solution: Install dependencies
pip install -r requirements.txt
```

**2. 429 Rate Limit Error**
```
⚠️ Rate limited by Reddit. Waiting 10 seconds...
```
- **Cause:** Too many requests too fast
- **Solution:** Already handled automatically (10s wait)
- **Prevention:** Increase `self.request_delay` in `scrapers/reddit.py`

**3. No Opportunities Found**
```
✅ Extracted 0 problems
```
- **Cause:** Keywords too specific or no matching posts
- **Solution:**
  - Use broader keywords
  - Try different problem phrases
  - Check Reddit manually if posts exist

**4. Web UI Not Loading**
```
Connection refused
```
- **Solution:**
  - Make sure Flask is running: `python api.py`
  - Check port 5000 is not used: `netstat -ano | findstr :5000`
  - Try different port: Edit `api.py` line `app.run(port=5001)`

**5. Post Content Not Scrollable**
- **Cause:** Old results before scrollable feature
- **Solution:** Run new batch research to get `full_text` field

**6. JSON Decode Error**
```
JSONDecodeError: Expecting value
```
- **Solution:**
  - Reddit API might be down (try again later)
  - Check internet connection
  - Verify URL in browser: `https://www.reddit.com/search.json?q=test`

**7. Empty JSON Files**
- **Cause:** Scraper returned no results
- **Solution:**
  - Verify keywords are valid
  - Check Reddit is accessible
  - Try manual search: `https://www.reddit.com/search/?q=your+keyword`

---

## 📈 Best Practices

### Keyword Selection

✅ **Good Keywords:**
- "n8n workflow breaks" (specific problem)
- "Zapier rate limit problem" (error type)
- "Make.com debugging issues" (pain point)
- "webhook automation fails" (common issue)

❌ **Bad Keywords:**
- "n8n" (too broad, gets non-problem posts)
- "automation" (too general)
- "best tool" (gets recommendation posts, not problems)

### Research Frequency

- **Weekly:** Run full batch research to discover new trends
- **Bi-weekly:** Check specific tool problems
- **Monthly:** Full scan of all tools in ecosystem

### Result Analysis

1. **Filter by score:** Focus on 30+ opportunities first
2. **Check engagement:** 50+ upvotes = validated problem
3. **Read full post:** Click URL to see context
4. **Validate demand:** Search for similar complaints
5. **Check solutions:** See if existing tools solve it poorly

### Building Solutions

1. **Start with 35+ scores:** Highest confidence opportunities
2. **Build MVP first:** Simple solution, fast to market
3. **Share with complainers:** Find original posters, offer solution
4. **Iterate based on feedback:** Improve from real user input
5. **Monetize early:** Test willingness to pay

---

## 🚀 Advanced Usage

### Automated Scheduling

**Windows Task Scheduler:**
```powershell
# Create task
schtasks /create /tn "TORUKMACTO Weekly" /tr "python s:\Engineering\2026\one\mock\torukmacto\run.py batch-reddit --limit 20" /sc weekly /d SUN /st 09:00
```

**Linux Cron:**
```bash
# Edit crontab
crontab -e

# Add weekly job (Sundays at 9 AM)
0 9 * * 0 cd /path/to/torukmacto && python run.py batch-reddit --limit 20
```

### Email Notifications

**Add to `run.py`:**
```python
import smtplib
from email.mime.text import MIMEText

def send_email_report(results):
    msg = MIMEText(f"Found {len(results)} opportunities!")
    msg['Subject'] = 'TORUKMACTO Weekly Report'
    msg['From'] = 'your@email.com'
    msg['To'] = 'your@email.com'
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('your@email.com', 'password')
        server.send_message(msg)
```

### Cloud Deployment

**Deploy to Railway/Render:**
1. Create `Procfile`: `web: python api.py`
2. Push to GitHub
3. Connect Railway to repo
4. Set environment variables
5. Deploy

**Cost:** $0-5/month

---

## 📝 File Formats

### research_keywords.json
```json
{
  "reddit_keywords": [
    "keyword 1",
    "keyword 2"
  ]
}
```

### reddit_research_final_*.json
```json
{
  "research_completed_at": "2026-01-17T17:27:53",
  "keywords_file": "research_keywords.json",
  "total_keywords": 6,
  "keyword_summary": {
    "n8n workflow breaks": {
      "total_posts": 5,
      "problems_found": 2,
      "opportunities_found": 2,
      "top_opportunity_score": 32.0
    }
  },
  "total_opportunities": 20,
  "top_10_opportunities": [
    {
      "id": "1m2qkjn",
      "source": "reddit",
      "url": "https://reddit.com/...",
      "original_title": "Title",
      "problem_statement": "Problem...",
      "full_text": "Complete post text...",
      "category": "Documentation",
      "tools_mentioned": ["claude", "make"],
      "engagement": {
        "reactions": 156,
        "comments": 91
      },
      "opportunity_score": {
        "pain": 4,
        "pervasiveness": 10,
        "proximity": 6.0,
        "payment": 5.0,
        "plausibility": 9,
        "total": 34.0
      },
      "recommendation": "🔥 HIGH OPPORTUNITY",
      "research_keyword": "Make.com debugging issues"
    }
  ]
}
```

---

## 🎯 Success Workflow

```
Week 1: Discovery
├── Run batch research
├── Review top 10 opportunities
└── Pick 2-3 high-scoring problems (30+)

Week 2: Validation
├── Read original Reddit posts
├── Find similar complaints
├── Check existing solutions
└── Validate people will pay

Week 3: Building
├── Design simple MVP
├── Build core features
└── Create landing page

Week 4: Launch
├── Share with Reddit complainers
├── Post in relevant subreddits
├── Collect feedback
└── Get first customers

Week 5+: Iterate
├── Improve based on feedback
├── Add requested features
├── Scale marketing
└── Grow revenue
```

---

## 🆘 Support & Resources

### Documentation Files
- `README.md` - Original project documentation
- `readme_torukmacto.md` - This complete guide
- `BATCH_REDDIT_RESEARCH.md` - Batch research guide
- `UI_GUIDE.md` - Web UI documentation
- `RATE_LIMIT_FIXES.md` - Rate limiting details

### Key Files to Modify
- `research_keywords.json` - Your search keywords
- `config.py` - Tools, repos, general config
- `processors/extractor.py` - Problem extraction logic
- `processors/scorer.py` - Scoring weights
- `static/styles.css` - UI theme

### Debug Mode

**Enable verbose logging:**
```python
# In run.py (top of file)
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🎉 Quick Start Checklist

- [ ] Install Python 3.8+
- [ ] Clone/download project
- [ ] `pip install -r requirements.txt`
- [ ] `python run.py demo` (test it works)
- [ ] Edit `research_keywords.json` (add your keywords)
- [ ] `python run.py batch-reddit --limit 5` (run research)
- [ ] `python api.py` (start web UI)
- [ ] Open `http://localhost:5000` (view results)
- [ ] Review opportunities, pick one to build
- [ ] Build MVP, get customers, make money! 💰

---

**🦅 "See problems others can't see. Build solutions people will pay for."**

That's TORUKMACTO. Happy hunting! 🚀

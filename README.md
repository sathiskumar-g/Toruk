# 🔍 TORUKMACTO - Problem Research Engine

**"Find real, painful, monetizable problems in the AI tools ecosystem"**

---

## 📖 What Is This Project?

**TORUKMACTO** is an automated problem discovery tool that:

1. **Scrapes** online sources (Hacker News, GitHub Issues) for developer complaints
2. **Extracts** the core problems from those complaints
3. **Scores** each problem as a business opportunity using the "5PM Fit" framework
4. **Reports** the top opportunities to you as JSON files

**Goal:** Give you a continuous stream of validated problem ideas so you can build AI tools that people actually want and will pay for.

---

## 🎯 What Will This Do?

### Example Workflow:

```bash
# You run:
python run.py search "langchain"

# The tool will:
# 1. Search Hacker News for posts about "langchain" + problem keywords
# 2. Search GitHub Issues for "langchain bug OR error"
# 3. Extract ~20-50 problem statements
# 4. Score each problem on:
#    - Pain (how much it hurts)
#    - Pervasiveness (how many people have it)
#    - Proximity (are they your target customers?)
#    - Payment (will they pay to solve it?)
#    - Plausibility (can you build a solution?)
# 5. Save a report to data/search_langchain_20260117_143022.json
# 6. Print the TOP 5 opportunities to your terminal
```

### What You Get:

**Terminal Output:**
```
🎯 TOP OPPORTUNITIES REPORT
============================================================

#1 [7.8/10] LangChain documentation is terrible, spent 3 days...
   📊 Pain: 8.0 | Pervasive: 6.5 | Payment: 8.0
   📂 Category: Documentation | Tools: ['langchain']
   🔗 https://news.ycombinator.com/item?id=12345678
   🔥 HIGH OPPORTUNITY - Worth pursuing immediately
```

**JSON File (data/search_langchain_*.json):**
```json
{
  "topic": "langchain",
  "problems_found": 23,
  "top_opportunities": [
    {
      "problem_statement": "LangChain documentation examples don't work...",
      "pain_score": 8,
      "opportunity_score": {
        "pain": 8.0,
        "pervasiveness": 6.5,
        "proximity": 7.5,
        "payment": 8.0,
        "plausibility": 9.0,
        "total": 7.8
      },
      "category": "Documentation",
      "tools_mentioned": ["langchain"],
      "url": "https://news.ycombinator.com/item?id=...",
      "engagement": {
        "reactions": 45,
        "comments": 12
      }
    }
  ]
}
```

---

## 🛠️ How Does It Work?

### Architecture:

```
┌──────────────┐
│   run.py     │  ← CLI entry point (you run this)
└──────┬───────┘
       │
       ├──→ scrapers/
       │    ├─ hackernews.py    → FREE Algolia API (10,000 req/hr)
       │    └─ github_issues.py → FREE GitHub API (60 req/hr, 5000 with token)
       │
       ├──→ processors/
       │    ├─ extractor.py  → Finds problem keywords, categorizes
       │    └─ scorer.py     → Scores using 5PM Fit framework
       │
       └──→ data/
            └─ search_*.json  → Results saved here
```
Installation & Usage:
# 1. Install dependencies (one-time, ~10 seconds)
cd s:\Engineering\2026\one\mock\torukmacto
pip install -r requirements.txt

# 2. Run quick demo (already tested - works!)
python run.py demo

# 3. Search specific topics
python run.py search "n8n"
python run.py search "openai api"

# 4. Full scan of all 21 tools
python run.py scan --all

# 5. GitHub repos only
python run.py scan --github



### Step-by-Step Flow:

1. **You run a command:** `python run.py search "n8n"`
2. **Scrapers fetch data:**
   - HackerNewsScraper searches HN for "n8n problem", "n8n bug", etc.
   - GitHubIssuesScraper searches all GitHub for "n8n bug OR error"
3. **Extractor processes raw data:**
   - Filters posts that contain problem keywords ("frustrated", "broken", "doesn't work")
   - Extracts the core problem statement
   - Categorizes (API Integration, Documentation, Performance, etc.)
   - Calculates initial pain score
4. **Scorer evaluates opportunities:**
   - Scores each problem on 5 dimensions (Pain, Pervasiveness, Proximity, Payment, Plausibility)
   - Calculates weighted total score (1-10)
   - Ranks all problems by score
5. **Results are saved:**
   - JSON file with full data
   - Terminal report with top 5-10 opportunities
6. **You review and decide:**
   - Look at high-scoring problems
   - Click URLs to read original posts
   - Decide which problem to solve

---

## ✅ What Do You Need to Add?

### ✅ NOTHING! (For MVP)

The tool works **out of the box** with **FREE APIs** and **no API keys required**.

### 🔧 Optional Additions (For Better Results):

#### 1. **GitHub Personal Access Token** (Recommended)
- **Why?** Increases rate limit from 60 req/hr to 5,000 req/hr
- **Cost:** FREE
- **How to add:**
  1. Go to https://github.com/settings/tokens
  2. Click "Generate new token (classic)"
  3. Select scope: `public_repo` (read-only)
  4. Copy the token
  5. Open `scrapers/github_issues.py`
  6. Change line 2 in `run.py`:
     ```python
     # Before:
     gh = GitHubIssuesScraper()
     
     # After:
     gh = GitHubIssuesScraper(token="ghp_your_token_here")
     ```

#### 2. **OpenAI/Claude API Key** (Future Enhancement)
- **Why?** Use AI to extract problems more accurately (better than keyword matching)
- **Cost:** ~$0.001 per problem analyzed
- **Not needed for MVP** - current keyword-based extraction works fine
- Will add this in V2 if you want

#### 3. **More Scrapers** (Future)
- Product Hunt (requires API key - FREE)
- Reddit (costs $0.24/1000 calls now 😢)
- Indie Hackers (web scraping - no API)

---

## 📦 Do You Need to Install Anything?

### Yes - Just 3 Python Packages:

```powershell
# Navigate to the project folder
cd s:\Engineering\2026\one\mock\torukmacto

# Install dependencies (takes ~10 seconds)
pip install -r requirements.txt
```

**What gets installed:**
- `requests` - for making HTTP requests to APIs
- `beautifulsoup4` - for parsing HTML (not used in MVP, but ready for future web scraping)
- `python-dateutil` - for parsing dates from API responses

**Total size:** ~5 MB
**Cost:** FREE
**Time:** 10 seconds

---

## 🚀 How to Use (Step-by-Step)

### Option 1: Quick Demo (30 seconds)

```powershell
cd s:\Engineering\2026\one\mock\torukmacto
python run.py demo
```

**What happens:**
1. Searches Hacker News for "langchain" problems
2. Extracts ~10-20 problems
3. Scores them
4. Prints top 5 opportunities to terminal
5. Saves results to `data/search_langchain_*.json`

**Output:** You'll see a report in your terminal + a JSON file saved.

---

### Option 2: Search a Specific Topic

```powershell
# Search for problems related to a tool
python run.py search "n8n"
python run.py search "openai api"
python run.py search "langchain memory"

# With custom limit
python run.py search "zapier" --limit 100
```

**What happens:**
- Searches Hacker News + GitHub for your topic
- Finds problems related to that topic
- Scores and ranks them
- Saves to `data/search_<topic>_<timestamp>.json`

**Use this when:** You want to research a specific tool or area.

---

### Option 3: Full Scan of All Tools

```powershell
python run.py scan --all
```

**What happens:**
- Scans ALL 21 tools in `config.py` (langchain, n8n, zapier, openai, etc.)
- For each tool: finds top 3 problems
- Ranks ALL problems across all tools
- Prints top 10 overall opportunities
- Saves to `data/full_scan_<timestamp>.json`

**Duration:** ~10-15 minutes (rate limits)
**Use this when:** You want a weekly/monthly scan to discover new opportunities.

---

### Option 4: GitHub Repos Scan

```powershell
python run.py scan --github
```

**What happens:**
- Scans the 8 repos in `config.py` (langchain-ai/langchain, n8n-io/n8n, etc.)
- Finds issues with high reactions/comments (= painful problems)
- Scores and ranks them
- Saves to `data/github_scan_<timestamp>.json`

**Use this when:** You want to focus on GitHub issues (often more detailed than HN posts).

---

## 🔄 Do You Need to Run This Tool Each Time?

### Yes, But You Can Automate It!

The tool **does not run continuously** - it runs when you execute it.

### Manual Usage:
```powershell
# Run once per week to discover new problems
python run.py scan --all
```

### Automated Usage (Recommended):

**Option A: Windows Task Scheduler**
1. Open Task Scheduler
2. Create Task: "TORUKMACTO Weekly Scan"
3. Trigger: Every Sunday at 9 AM
4. Action: Run `python s:\Engineering\2026\one\mock\torukmacto\run.py scan --all`
5. Output saved to `data/` folder automatically

**Option B: Manual Weekly Routine**
- Every Sunday morning: `python run.py scan --all`
- Review the JSON file in `data/`
- Pick the top 3 opportunities to research further

**Option C: Cloud Hosting (Advanced)**
- Deploy to AWS Lambda / Railway / Render
- Schedule: Daily or weekly
- Email results to yourself
- Cost: ~$0-5/month

---

## 🎯 Complete Usage Flow Example

### Scenario: "I want to find a problem to solve"

```powershell
# Step 1: Navigate to project
cd s:\Engineering\2026\one\mock\torukmacto

# Step 2: Install dependencies (first time only)
pip install -r requirements.txt

# Step 3: Run quick demo to test it works
python run.py demo

# Step 4: Search a tool you're interested in
python run.py search "n8n workflow"

# Step 5: Review terminal output
# You'll see:
# 🎯 TOP OPPORTUNITIES REPORT
# #1 [8.2/10] n8n webhooks randomly fail...
# #2 [7.5/10] n8n self-hosting is confusing...

# Step 6: Open the saved JSON file
# Location: data/search_n8n_workflow_20260117_143022.json
# Contains: Full details, URLs, engagement metrics

# Step 7: Click URLs to read original posts
# Validate the problem is real

# Step 8: Decide which problem to solve!
```

---

## 📊 Understanding the Output

### Terminal Report:
```
#1 [7.8/10] LangChain documentation is terrible...
   📊 Pain: 8.0 | Pervasive: 6.5 | Payment: 8.0
   📂 Category: Documentation | Tools: ['langchain']
   🔗 https://news.ycombinator.com/item?id=12345678
   🔥 HIGH OPPORTUNITY - Worth pursuing immediately
```

**What each line means:**
- `[7.8/10]` - Overall opportunity score (higher = better)
- `Pain: 8.0` - How much the problem hurts (1-10)
- `Pervasive: 6.5` - How many people have it (1-10)
- `Payment: 8.0` - Likelihood they'll pay to solve it (1-10)
- `Category` - Type of problem (Documentation, API Integration, etc.)
- `Tools` - Which tools are involved
- `🔥 HIGH OPPORTUNITY` - Recommendation (🔥 = pursue, ✅ = explore, ⚠️ = maybe, ❌ = skip)

### JSON File Fields:
```json
{
  "problem_statement": "The actual problem",
  "opportunity_score": {
    "pain": 8.0,
    "pervasiveness": 6.5,
    "proximity": 7.5,    // Are they your customers?
    "payment": 8.0,
    "plausibility": 9.0, // Can you build it?
    "total": 7.8
  },
  "category": "Documentation",
  "tools_mentioned": ["langchain"],
  "matched_keywords": ["frustrated", "doesn't work"],
  "engagement": {
    "reactions": 45,
    "comments": 12
  },
  "url": "https://...",
  "author": "dev123",
  "created_at": "2026-01-15T10:30:00Z"
}
```

---

## 🔐 API Keys Summary

| Service | Required? | Cost | Rate Limit | How to Add |
|---------|-----------|------|------------|------------|
| **Hacker News** | ❌ No | FREE | 10,000 req/hr | Built-in |
| **GitHub (no token)** | ❌ No | FREE | 60 req/hr | Built-in |
| **GitHub (with token)** | ⭐ Recommended | FREE | 5,000 req/hr | See "Optional Additions" above |
| **OpenAI/Claude** | 🔮 Future | ~$0.001/problem | N/A | Not implemented yet |

**TLDR:** You can start using it RIGHT NOW with ZERO API keys!

---

## 🎓 What You'll Learn

By using this tool, you'll discover:

1. **What problems people actually have** (not what you imagine)
2. **Which problems are most painful** (high opportunity scores)
3. **Which problems people will pay for** (payment score)
4. **Which problems you can solve** (plausibility score)
5. **How to validate ideas before building** (engagement metrics)

**This is your "idea validation engine"** - run it weekly to stay on top of real problems in the AI tools space.

---

## 📁 Project Structure

```
torukmacto/
├── README.md                      ← You are here
├── MASTER_PROBLEM_RESEARCH.md     ← Full research methodology
├── MVP_SCOPE.md                   ← MVP scope and features
├── requirements.txt               ← Python dependencies
├── config.py                      ← Tools to monitor, keywords, repos
├── run.py                         ← Main CLI entry point
│
├── scrapers/                      ← Data collection
│   ├── __init__.py
│   ├── base.py                    ← Base scraper class
│   ├── hackernews.py              ← HN Algolia API scraper
│   └── github_issues.py           ← GitHub Issues API scraper
│
├── processors/                    ← Data processing
│   ├── __init__.py
│   ├── extractor.py               ← Problem extraction
│   └── scorer.py                  ← 5PM Fit scoring
│
├── prompts/                       ← AI prompts (future)
│   ├── extraction.txt             ← For GPT/Claude extraction
│   └── scoring.txt                ← For GPT/Claude scoring
│
└── data/                          ← Results (gitignored)
    ├── search_*.json              ← Search results
    ├── full_scan_*.json           ← Full scan results
    └── github_scan_*.json         ← GitHub scan results
```

---

## 🚀 Next Steps

### 1. Run the Demo Now:
```powershell
cd s:\Engineering\2026\one\mock\torukmacto
pip install -r requirements.txt
python run.py demo
```

### 2. Pick a Tool to Research:
```powershell
python run.py search "n8n"
python run.py search "langchain"
python run.py search "openai"
```

### 3. Review Results:
- Read terminal report
- Open JSON file in `data/`
- Click URLs to read original posts
- Validate the problems are real

### 4. Build a Solution:
- Pick a high-scoring problem (7.5+)
- Build a simple MVP
- Share with people who have the problem
- Get paid!

---

## ❓ FAQ

**Q: Will this cost me money?**
A: No! All APIs used are FREE. Optional: GitHub token (free) increases rate limits.

**Q: Do I need to know Python?**
A: Not really. Just run the commands. The code is well-commented if you want to learn.

**Q: How often should I run this?**
A: Weekly or bi-weekly is good. Use `python run.py scan --all` for a full market scan.

**Q: Can I add more sources?**
A: Yes! You can add Product Hunt, Reddit, Indie Hackers, etc. See `MVP_SCOPE.md` for future plans.

**Q: What if I get rate limited?**
A: Add a GitHub token (see "Optional Additions"). Or wait an hour. Free APIs have generous limits.

**Q: Can I customize what problems to look for?**
A: Yes! Edit `config.py`:
  - `TOOLS_TO_MONITOR` - add/remove tools
  - `PROBLEM_KEYWORDS` - add keywords like "annoying", "painful"
  - `GITHUB_REPOS` - add repos to scan

**Q: Is this legal?**
A: Yes! We use official public APIs. No TOS violations. All data is publicly available.

---

## 🎯 Your Workflow

```
┌─────────────────────────────────────────────┐
│  1. Run tool weekly: python run.py scan    │
│                                             │
│  2. Review top 10 opportunities             │
│                                             │
│  3. Click URLs, read original posts         │
│                                             │
│  4. Pick 1-2 problems to solve              │
│                                             │
│  5. Build simple MVP                        │
│                                             │
│  6. Share with people who have problem      │
│                                             │
│  7. Get feedback + early customers          │
│                                             │
│  8. Iterate and improve                     │
│                                             │
│  9. Earn money 💰                            │
└─────────────────────────────────────────────┘
```

---

## 🆕 NEW: Batch Reddit Research

Search Reddit with custom keywords and aggregate all results!

### Quick Start
```bash
# 1. Edit keywords
nano research_keywords.json

# 2. Run batch research
python run.py batch-reddit --limit 20

# 3. View results as table
python json_to_table.py data/reddit_research_final_*.json
```

### Features
- ✅ Custom keyword list
- ✅ Searches ALL of Reddit (not just specific subreddits)
- ✅ Individual results per keyword
- ✅ Final aggregate report with ALL opportunities ranked
- ✅ Beautiful table view converter

See [BATCH_REDDIT_RESEARCH.md](BATCH_REDDIT_RESEARCH.md) for full guide.

---

**🎯 "See problems others can't see. Build solutions people will pay for."**

That's TORUKMACTO. 🦅

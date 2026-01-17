# 🧠 MASTER PROBLEM RESEARCH ENGINE

## Automated Problem Discovery for AI Tools & SaaS

**Created:** January 17, 2026  
**Goal:** Find real, painful, monetizable problems to build AI tools  
**Approach:** Problem-first, not solution-first

---

## 📌 CORE PHILOSOPHY

> "Don't build what you think is cool. Build what people are screaming about."

### The 3 End Goals:
1. **Learn** - Deep understanding of AI tools ecosystem
2. **Find** - Real problems worth solving
3. **Earn** - Build tools or offer AAA services

---

## 🎯 WHAT WE'RE BUILDING

An **Automatic Problem Researcher** that:

| Step | Action | Output |
|------|--------|--------|
| 1 | Scan sources | Raw posts/reviews |
| 2 | Extract complaints | Verbatim quotes |
| 3 | Structure problems | Actionable statements |
| 4 | Score viability | Monetization potential |
| 5 | Store & search | Problem database |
| 6 | Surface opportunities | Build recommendations |

---

## 🔍 TARGET PROBLEM DOMAINS

### AI Platforms (Where people complain)

| Category | Tools to Monitor |
|----------|------------------|
| **LLM Providers** | OpenAI, Claude, Gemini, Mistral, LLaMA |
| **AI Frameworks** | LangChain, LangGraph, CrewAI, AutoGen |
| **AI Apps** | ChatGPT, Perplexity, Copilot, Cursor |
| **Automation** | n8n, Zapier, Make, Pipedream |
| **Dev Tools** | GitHub Copilot, Cursor, Cody |

### Problem Categories to Track

| Category | Example Complaints |
|----------|-------------------|
| **Reliability** | "It works 80% of the time" |
| **Debugging** | "No idea why it failed" |
| **Cost** | "Bill was 10x what I expected" |
| **Memory** | "Forgets context every time" |
| **Integration** | "Breaks when I connect X to Y" |
| **Security** | "Can't control what data it sees" |
| **Scalability** | "Works for 10 users, dies at 100" |
| **DX** | "Docs are terrible" |

---

## 📊 PROBLEM EVALUATION FRAMEWORK

### The Painkiller Test ✅

Every problem MUST answer YES to:

```
□ Does it save TIME?
□ Does it save MONEY?
□ Does it save EFFORT?
□ Does it MAKE money?
□ Is the pain FREQUENT?
□ Is the pain URGENT?
□ Is the pain COSTLY if unsolved?
```

### Good Problem Criteria

| Criteria | Question | Score (1-5) |
|----------|----------|-------------|
| **Prevalent** | Do many people face this? | __ |
| **Growing** | Is it getting worse? | __ |
| **Frequent** | Does it happen often? | __ |
| **Valuable** | Will people pay to fix it? | __ |
| **Clear ICP** | Can you name who has this? | __ |

### 5PM Fit Score

| Factor | Weight | Description |
|--------|--------|-------------|
| **Pain** | 25% | How bad is it? |
| **Purchasing** | 20% | Can they afford solution? |
| **Market** | 20% | How big is the market? |
| **Product** | 20% | Can you build it? |
| **Personal** | 15% | Can YOU specifically build it? |

---

## 🔎 DATA SOURCES (Free/Accessible)

### Tier 1: Free APIs ✅

| Source | API | What to Get |
|--------|-----|-------------|
| **Hacker News** | Free | Posts, comments |
| **GitHub** | Free | Issues, discussions |
| **Product Hunt** | Free | Comments, reviews |
| **Stack Overflow** | Free | Questions, answers |
| **Dev.to** | Free | Articles, comments |

### Tier 2: Scraping (Careful) ⚠️

| Source | Method | Risk |
|--------|--------|------|
| **Reddit** | Google cache or manual | Medium |
| **G2 Reviews** | Web scraping | Low |
| **Capterra** | Web scraping | Low |
| **Indie Hackers** | Web scraping | Low |

### Tier 3: Manual Collection 📝

| Source | Method |
|--------|--------|
| **Twitter/X** | Manual search + copy |
| **Discord** | Join servers, observe |
| **Slack communities** | Join, observe |

---

## 🔑 SEARCH QUERY MATRIX

### Problem-Revealing Queries

```
# Frustration patterns
"I wish there was a tool for"
"why is there no tool"
"this is so frustrating"
"doesn't work"
"fails every time"
"broke my workflow"

# Limitation patterns
"limitations of [TOOL]"
"[TOOL] can't do"
"biggest problem with [TOOL]"
"[TOOL] is missing"

# Cost patterns
"[TOOL] is too expensive"
"[TOOL] cost me"
"[TOOL] bill was"
"cheaper alternative to [TOOL]"

# Technical patterns
"[TOOL] error"
"[TOOL] bug"
"[TOOL] no logs"
"[TOOL] debugging"
"[TOOL] memory issue"
"[TOOL] rate limit"
```

### Reddit-Specific Searches (via Google)

```
site:reddit.com r/n8n "frustrated"
site:reddit.com r/OpenAI "problem with"
site:reddit.com r/ChatGPT "doesn't work"
site:reddit.com r/automation "fails"
site:reddit.com r/SaaS "I wish"
site:reddit.com r/Artificial "limitation"
```

### GitHub Issue Searches

```
repo:langchain-ai/langchain is:issue is:open "bug"
repo:n8n-io/n8n is:issue "feature request"
org:openai is:issue "error"
```

---

## 📋 PROBLEM EXTRACTION TEMPLATE

For every problem found, capture:

```json
{
  "id": "unique-id",
  "timestamp": "2026-01-17T10:00:00Z",
  
  "source": {
    "platform": "Reddit | HN | GitHub | G2",
    "url": "exact URL",
    "date_posted": "original post date"
  },
  
  "context": {
    "tool_name": "n8n | OpenAI | LangChain",
    "user_type": "developer | founder | marketer",
    "industry": "if mentioned"
  },
  
  "problem": {
    "direct_quote": "EXACT verbatim quote",
    "summary": "One sentence summary",
    "category": "Debugging | Cost | Memory | Integration",
    "severity": "low | medium | high | critical"
  },
  
  "signals": {
    "frequency": "isolated | repeating | trending",
    "urgency": "low | medium | high",
    "willingness_to_pay": "low | medium | high",
    "workaround_exists": true | false,
    "competitor_mentioned": "name if any"
  },
  
  "scores": {
    "pain_intensity": 1-10,
    "market_demand": 1-10,
    "monetization": 1-10,
    "build_feasibility": 1-10,
    "saturation": 1-10
  },
  
  "opportunity": {
    "type": "SaaS | Tool | Service | Integration",
    "effort": "weekend | month | quarter",
    "revenue_model": "subscription | one-time | usage"
  }
}
```

---

## 🧠 AI ANALYSIS PROMPTS

### Prompt 1: Extract Problems

```
Analyze this content and extract specific problems/complaints.

For each problem:
1. Quote the EXACT words (verbatim)
2. Identify the tool mentioned
3. Categorize the problem type
4. Rate severity (1-5)
5. Note if they mention willingness to pay

Content:
[PASTE CONTENT]

Return as JSON array.
```

### Prompt 2: Score Opportunity

```
Evaluate this problem for business opportunity:

Problem: [PROBLEM STATEMENT]
Source: [WHERE FOUND]
Frequency: [HOW OFTEN MENTIONED]

Score 1-10 for:
- Pain intensity
- Market size
- Monetization potential
- Build complexity (inverse)
- Competition saturation (inverse)

Recommend: Build SaaS / Offer Service / Skip

Explain reasoning briefly.
```

### Prompt 3: Cluster Problems

```
Group these problems by theme:

[LIST OF PROBLEMS]

For each cluster:
- Name the theme
- Count occurrences
- Identify common tool
- Suggest solution type
- Rate opportunity (A/B/C)
```

---

## 🏗️ MVP ARCHITECTURE

### Phase 1: Manual + AI (Week 1)

```
You (Manual)          This Tool (AI)
    │                      │
    ├── Copy content ──────┤
    │                      ├── Extract problems
    │                      ├── Score them
    │                      └── Save to JSON
    │                      │
    └── Review output ◄────┘
```

### Phase 2: Semi-Automated (Week 2-3)

```
Scraper (Python)       AI Layer            Database
    │                      │                   │
    ├── HN API ────────────┤                   │
    ├── GitHub API ────────┼── Claude API ─────┼── JSON/SQLite
    ├── Google Search ─────┤                   │
    └── Review sites ──────┘                   │
```

### Phase 3: Full Automation (Month 2+)

```
┌─────────────────────────────────────────────────────────┐
│                 PROBLEM RESEARCH ENGINE                  │
├─────────────────────────────────────────────────────────┤
│  Collectors          Processors         Storage          │
│  ├── HN              ├── Extractor      ├── PostgreSQL   │
│  ├── GitHub          ├── Scorer         ├── Vector DB    │
│  ├── Google          ├── Clusterer      └── Search       │
│  └── Reviews         └── Trend Detector                  │
│                                                          │
│  Outputs                                                 │
│  ├── Dashboard                                           │
│  ├── Daily digest email                                  │
│  ├── Opportunity alerts                                  │
│  └── API for your apps                                   │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 FILE STRUCTURE

```
torukmacto/
├── MASTER_PROBLEM_RESEARCH.md    # This file
├── MVP_SCOPE.md                   # Simple scope doc
├── scrapers/
│   ├── __init__.py
│   ├── hackernews.py              # HN API scraper
│   ├── github_issues.py           # GitHub scraper
│   └── google_search.py           # Google SERP
├── processors/
│   ├── __init__.py
│   ├── extractor.py               # AI extraction
│   └── scorer.py                  # Opportunity scoring
├── data/
│   ├── problems.json              # Collected problems
│   └── opportunities.json         # Scored opportunities
├── prompts/
│   └── extraction_prompts.md      # AI prompts
└── run.py                         # Main entry point
```

---

## 🎯 SUCCESS METRICS

### Weekly Targets

| Metric | Target |
|--------|--------|
| Problems discovered | 50+ |
| High-score opportunities | 5+ |
| New patterns identified | 3+ |
| Validated with real people | 2+ |

### Monthly Targets

| Metric | Target |
|--------|--------|
| Problem database size | 200+ |
| Build-worthy ideas | 10+ |
| Actually started building | 1+ |
| Revenue from learning | $0 → $X |

---

## 🚀 ACTION PLAN

### This Week

- [ ] Run MVP scraper on Hacker News
- [ ] Collect 50 problems manually
- [ ] Score top 10 opportunities
- [ ] Pick 1 to explore deeper

### This Month

- [ ] Automate 3 data sources
- [ ] Build problem database (500+)
- [ ] Identify top 5 opportunities
- [ ] Start building #1 opportunity

### This Quarter

- [ ] Launch first tool/service
- [ ] Generate first revenue
- [ ] Refine research system
- [ ] Scale what works

---

## 💡 KEY INSIGHTS TO REMEMBER

1. **Problems > Solutions** - Find pain first, build second
2. **Quotes > Summaries** - Verbatim complaints are gold
3. **Frequency > Intensity** - Repeated small pain beats rare big pain
4. **Action > Research** - Don't over-research, start building
5. **Revenue > Users** - Paying customers validate, free users don't

---

## 🔗 RESOURCES

### Communities to Monitor

- r/SaaS, r/automation, r/OpenAI, r/n8n
- Hacker News (daily front page)
- Indie Hackers
- Twitter AI accounts
- Discord: LangChain, n8n, AI builders

### Tools to Use

- Claude/GPT for analysis
- Python for scraping
- Notion/Airtable for database
- This system for discovery

---

*"The best products solve problems people are already complaining about."*

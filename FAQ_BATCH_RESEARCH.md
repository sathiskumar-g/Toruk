# Understanding Your Batch Reddit Research System

## 1. Does It Only Search Reddit?

**YES!** The `batch-reddit` command searches **ONLY Reddit**, not HN or GitHub.

```bash
python run.py batch-reddit    # ✅ Searches ONLY Reddit
python run.py search "topic"   # Searches Reddit + HN + GitHub
```

### Why Only Reddit?
- Focused research on ONE platform
- Reddit has different discussion style than HN
- You control which platform to search
- Faster results (fewer API calls)

---

## 2. What Does `--limit 20` Mean?

`--limit 20` = **Maximum 20 Reddit posts PER keyword**

### Example:
```json
{
  "reddit_keywords": [
    "I wish there was a tool for",
    "too expensive",
    "rate limit"
  ]
}
```

With `--limit 20`:
- "I wish there was a tool for" → Up to 20 posts
- "too expensive" → Up to 20 posts  
- "rate limit" → Up to 20 posts
- **Total**: Up to 60 posts (3 keywords × 20)

### Why Limit It?

| Limit | Speed | Results | Use Case |
|-------|-------|---------|----------|
| 5-10  | ⚡⚡⚡ Fast | Quick test | Testing keywords |
| 20-30 | ⚡⚡ Medium | Balanced | Normal research |
| 50-100| ⚡ Slow | Deep dive | Comprehensive study |

**Recommendation:** Use `--limit 20` for normal research

### Commands:
```bash
# Fast test (5 posts per keyword)
python run.py batch-reddit --limit 5

# Normal research (20 posts per keyword)
python run.py batch-reddit --limit 20

# Deep research (50 posts per keyword)
python run.py batch-reddit --limit 50
```

---

## 3. What's Already in the JSON Results?

### ✅ Already Included:

Your JSON files **ALREADY contain**:
- **Upvotes**: `engagement.reactions`
- **Comment count**: `engagement.comments`
- **Post author**: `author`
- **Subreddit**: `subreddit` (in full results)
- **Post URL**: `url`
- **Post title**: `original_title`

### Example JSON Structure:
```json
{
  "id": "1ommuxy",
  "source": "reddit",
  "url": "https://www.reddit.com/r/selfhosted/comments/1ommuxy/...",
  "original_title": "I'm the author of LocalAI...",
  "engagement": {
    "reactions": 868,     // ← UPVOTES
    "comments": 122       // ← COMMENT COUNT
  },
  "author": "mudler_it",
  "subreddit": "selfhosted",
  "pain_score": 4,
  "opportunity_score": {
    "total": 32.0
  }
}
```

### 🆕 Now Adding: Comment Text

Updated system now fetches **actual comment text** from top posts:

```json
{
  "url": "https://www.reddit.com/...",
  "engagement": {
    "reactions": 868,
    "comments": 122
  },
  "top_comments": [           // ← NEW!
    {
      "text": "This is exactly what I needed!",
      "author": "user123",
      "points": 45
    },
    {
      "text": "Does it support GPT-4?",
      "author": "user456",
      "points": 32
    }
  ]
}
```

---

## 4. How to Read Your Results

### Method 1: JSON File (Raw Data)
```bash
# View raw JSON
cat data/reddit_research_final_20260117_134631.json
```

Good for:
- Programmatic processing
- Import into tools
- Full data access

### Method 2: Table View (Human Readable)
```bash
# Beautiful table format
python json_to_table.py data/reddit_research_final_20260117_134631.json
```

Shows:
- Keyword summary (posts/problems/score per keyword)
- Top opportunities ranked
- Upvotes, comments, scores

Good for:
- Quick review
- Sharing with team
- Making decisions

---

## 5. Complete Workflow Example

### Step 1: Create Keywords File
```json
{
  "reddit_keywords": [
    "I wish there was a tool for context store api",
    "no logging",
    "expensive API calls",
    "rate limit issues"
  ]
}
```

### Step 2: Run Research
```bash
# Run with 20 posts per keyword
python run.py batch-reddit --limit 20
```

**What happens:**
1. Searches Reddit for "I wish there was a tool for context store api" → 20 posts
2. Searches Reddit for "no logging" → 20 posts
3. Searches Reddit for "expensive API calls" → 20 posts
4. Searches Reddit for "rate limit issues" → 20 posts
5. Fetches top comments from each post
6. Extracts problems and scores them
7. Saves individual files + final aggregate

### Step 3: Review Results
```bash
# View as table
python json_to_table.py data/reddit_research_final_*.json
```

**You'll see:**
- Which keywords found the most opportunities
- Top scoring problems across ALL keywords
- Engagement metrics (upvotes + comments)
- Direct links to Reddit threads

### Step 4: Analyze
Look for:
- **High scores** (30+) = Strong opportunity
- **High engagement** (500+ upvotes) = Validated pain
- **Recent posts** = Current problem
- **Multiple similar posts** = Widespread issue

---

## 6. Understanding the Output

### Keyword Summary
```
┌──────────────────────┬────────┬───────────┬───────────────────┐
│ Keyword              │ Posts  │ Problems  │ Top Score         │
├──────────────────────┼────────┼───────────┼───────────────────┤
│ context store api    │ 20     │ 5         │ 35.0              │
│ expensive API calls  │ 20     │ 12        │ 34.0              │
│ no logging           │ 20     │ 3         │ 29.0              │
└──────────────────────┴────────┴───────────┴───────────────────┘
```

- **Posts**: Total Reddit posts found for this keyword
- **Problems**: How many were actual problems (filtered)
- **Top Score**: Best opportunity score from this keyword

### Opportunities Table
```
┌───────┬────────┬─────────────────┬─────────┬────────┐
│ Rank  │ Score  │ Title           │ Upvotes │ Comments│
├───────┼────────┼─────────────────┼─────────┼────────┤
│ 1     │ 35.0   │ Context API...  │ 1200    │ 245    │
│ 2     │ 34.0   │ API costs...    │ 890     │ 156    │
└───────┴────────┴─────────────────┴─────────┴────────┘
```

- **Score**: Opportunity score (higher = better)
- **Upvotes**: Reddit upvotes (more = more validated)
- **Comments**: Comment count (more = more discussion)

---

## 7. Quick Reference

### Commands
```bash
# Test with 5 results per keyword
python run.py batch-reddit --limit 5

# Normal research
python run.py batch-reddit --limit 20

# Deep research
python run.py batch-reddit --limit 50

# View results
python json_to_table.py data/reddit_research_final_*.json

# Save to file
python json_to_table.py data/reddit_research_final_*.json -o report.txt
```

### Data Location
- **Individual keywords**: `data/reddit_keyword_*.json`
- **Final aggregate**: `data/reddit_research_final_*.json`

### JSON Structure
```json
{
  "keyword": "your keyword",
  "opportunities": [
    {
      "url": "reddit URL",
      "original_title": "post title",
      "engagement": {
        "reactions": 868,      // upvotes
        "comments": 122        // comment count
      },
      "top_comments": [...],   // actual comments (NEW)
      "opportunity_score": {
        "total": 32.0
      }
    }
  ]
}
```

---

## 8. Common Questions

**Q: Why only 20 results per keyword?**
A: Balance between speed and thoroughness. 20 is usually enough to find the best opportunities.

**Q: Can I search ALL of Reddit without limits?**
A: Yes! Use `--limit 100` but it will be slower.

**Q: Do I get comment TEXT or just count?**
A: NOW BOTH! Updated system fetches top 10 comments from top 5 posts per keyword.

**Q: Does it search specific subreddits?**
A: No, it searches ALL of Reddit. The scraper adds context ("AI tools", "SaaS", "automation") to your keywords automatically.

**Q: How long does it take?**
A: ~15 seconds per keyword. 10 keywords = ~2.5 minutes.

---

**Your system is fully functional! 🚀**

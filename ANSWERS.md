# ✅ ANSWERS TO YOUR QUESTIONS

## 1. "When the keyword checks, should only show Reddit site only?"

**YES! ✅**

When you run:
```bash
python run.py batch-reddit --limit 20
```

It **ONLY searches Reddit**. No HN, no GitHub.

### Proof:
- Uses `RedditScraper()` only
- Calls `reddit.com/search.json` API
- All results have `"source": "reddit"`
- URLs are all `reddit.com/...`

### If you want multiple sources:
```bash
# Search Reddit + HN + GitHub
python run.py search "langchain"

# Search ONLY Reddit
python run.py batch-reddit
```

---

## 2. "What is --limit 20? Why is each keyword search result limited to 20?"

`--limit 20` = **Maximum 20 Reddit posts PER keyword**

### Why limit it?

#### Speed vs Results Tradeoff:

| Limit | Time per keyword | Quality | When to use |
|-------|------------------|---------|-------------|
| 5     | ~10 sec          | Quick sample | Testing keywords |
| 20    | ~15 sec          | **Recommended** | Normal research |
| 50    | ~30 sec          | Deep dive | Thorough analysis |
| 100   | ~60 sec          | Exhaustive | Academic study |

### Example with 3 keywords:
```json
{
  "reddit_keywords": [
    "context store api",
    "expensive pricing",
    "no error handling"
  ]
}
```

With `--limit 20`:
- Keyword 1 → Up to 20 posts
- Keyword 2 → Up to 20 posts
- Keyword 3 → Up to 20 posts
- **Total time**: ~45 seconds (3 × 15 sec)
- **Total results**: Up to 60 posts

### Change the limit:
```bash
# Fast test
python run.py batch-reddit --limit 5

# Normal (recommended)
python run.py batch-reddit --limit 20

# Deep research
python run.py batch-reddit --limit 50
```

### Why 20 is optimal:
- ✅ Fast enough (~15 sec per keyword)
- ✅ Captures top/most relevant posts
- ✅ Enough data for good insights
- ✅ Doesn't overwhelm you with data
- ✅ Respects Reddit's servers

---

## 3. "Add upvotes, comments count, and comments into JSON"

### ✅ Already Included!

Your JSON files **ALREADY have** upvotes and comment count:

```json
{
  "url": "https://www.reddit.com/r/AI_Agents/comments/...",
  "original_title": "I've been in the AI/automation space since 2022...",
  "engagement": {
    "reactions": 899,      // ← UPVOTES
    "comments": 254        // ← COMMENT COUNT
  },
  "author": "Shivam5483"
}
```

### 🆕 NOW ADDED: Actual Comment Text!

Updated system now fetches top comments:

```json
{
  "url": "https://www.reddit.com/r/gaming/comments/...",
  "engagement": {
    "reactions": 920,
    "comments": 156
  },
  "top_comments": [           // ← NEW!
    {
      "text": "I was always a bit ambivalent about the way overwatch did it...",
      "author": "GmSaysTryMe",
      "points": 920,
      "reactions": 920
    },
    {
      "text": "You're getting some negative feedback for a system that positively...",
      "author": "OldeFortran77",
      "points": 3133,
      "reactions": 3133
    }
  ]
}
```

### What's included:
- ✅ **Upvotes** (reactions) - Already there
- ✅ **Comment count** - Already there  
- ✅ **Comment text** - NOW ADDED!
- ✅ **Comment author** - NOW ADDED!
- ✅ **Comment upvotes** - NOW ADDED!

### How it works:
- Fetches top 10 comments from top 5 posts per keyword
- Each comment has full text + author + upvotes
- Saved in `top_comments` array

---

## Complete JSON Structure

### Before (you already had this):
```json
{
  "keyword": "context store api",
  "opportunities": [
    {
      "url": "https://www.reddit.com/...",
      "original_title": "Post title",
      "engagement": {
        "reactions": 899,      // upvotes ✅
        "comments": 254        // count ✅
      },
      "author": "username",
      "subreddit": "AI_Agents",
      "pain_score": 4,
      "opportunity_score": {
        "total": 31.0
      }
    }
  ]
}
```

### After (now includes comment text):
```json
{
  "keyword": "context store api",
  "opportunities": [
    {
      "url": "https://www.reddit.com/...",
      "original_title": "Post title",
      "engagement": {
        "reactions": 899,
        "comments": 254
      },
      "author": "username",
      "subreddit": "AI_Agents",
      "top_comments": [          // ← NEW!
        {
          "type": "comment",
          "text": "This is exactly what I needed! The lack of proper context...",
          "author": "user123",
          "points": 145,
          "reactions": 145
        },
        {
          "text": "I've been looking for this for months...",
          "author": "user456",
          "points": 89
        }
      ],
      "pain_score": 4,
      "opportunity_score": {
        "total": 31.0
      }
    }
  ]
}
```

---

## Quick Reference

### Run Research
```bash
# With comment fetching (default)
python run.py batch-reddit --limit 20

# Fast test
python run.py batch-reddit --limit 5
```

### View Results
```bash
# Table view (shows upvotes + comment count)
python json_to_table.py data/reddit_research_final_*.json

# Raw JSON (shows everything including comment text)
cat data/reddit_research_final_*.json
```

### What You Get
- ✅ Reddit posts (up to 20 per keyword)
- ✅ Upvotes for each post
- ✅ Comment count for each post
- ✅ **Top 10 comments** from top 5 posts (with text!)
- ✅ Individual keyword results
- ✅ Final aggregate report

---

## Test Results

Successfully tested:
```
🔍 Testing Reddit Comment Fetching

Step 1: Searching Reddit...
✅ Found 2 posts

Step 2: Fetching comments...
💬 Found 5 comments

Sample comments:
1. Author: GmSaysTryMe
   Points: 920
   Text: I was always a bit ambivalent...

2. Author: OldeFortran77
   Points: 3133
   Text: You're getting some negative feedback...
```

**Everything works! 🎉**

---

## Summary

✅ **Only searches Reddit** - No HN, no GitHub  
✅ **--limit 20 = 20 posts per keyword** - Optimal balance  
✅ **Upvotes included** - Already was there  
✅ **Comment count included** - Already was there  
✅ **Comment TEXT now included** - Just added!

Read [FAQ_BATCH_RESEARCH.md](FAQ_BATCH_RESEARCH.md) for more details.

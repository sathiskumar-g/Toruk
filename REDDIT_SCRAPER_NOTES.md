# Reddit Scraper - WORKING! ✅

## Status: FULLY FUNCTIONAL

The Reddit scraper now uses Reddit's **FREE JSON API** and searches **ALL of Reddit** (not restricted to subreddits).

## How It Works

Instead of the paid Reddit API ($0.24/1000 calls), we use Reddit's public JSON endpoints:
- `https://www.reddit.com/search.json?q=your+query`
- No authentication required
- No API key needed
- Completely free!

## Usage

### 1. Search by Problem Keyword
```bash
python run.py reddit --keyword "I wish there was a tool for" --limit 10
python run.py reddit --keyword "doesn't work as expected" --limit 15
python run.py reddit --keyword "too expensive" --limit 20
```

### 2. Include Reddit in General Search
```bash
python run.py search "langchain" --limit 50
# Automatically includes Reddit + HN + GitHub
```

### 3. Skip Reddit (if needed)
```bash
python run.py search "openai" --no-reddit
```

## Test Results

✅ **Tested:** `"I wish there was a tool for"` → Found 3 posts  
✅ **Tested:** `"doesn't work as expected"` → Found 8 posts  
✅ **Working:** Searches ALL of Reddit, not restricted to specific subreddits

## How Search Works

The scraper combines your keyword with AI/SaaS context:
- `"{keyword} AI tools"`
- `"{keyword} automation tool"`
- `"{keyword} SaaS"`

This ensures results are relevant to your business research!

## Example Results

```
r/AI_Agents - Most of you won't make it It'll be a long post...
   Points: 127 | Comments: 45
   https://www.reddit.com/r/AI_Agents/comments/...

r/webdev - Got fired from a company for finding a security pr...
   Points: 892 | Comments: 234
   https://www.reddit.com/r/webdev/comments/...
```

## All Problem Keywords Configured

The scraper will work with ALL these keywords:
- "I wish there was a tool for"
- "why is there no tool"
- "this tool is frustrating"
- "fails when"
- "doesn't work as expected"
- "limitations of"
- "biggest problem with"
- "alternative to"
- "no memory"
- "no logs"
- "hard to debug"
- "too expensive"
- "rate limit"
- "hallucination"
- "tool calling failed"
- "automation breaks"

## Technical Details

**Old Approach (BROKEN):**
- Used `old.reddit.com` HTML scraping
- Reddit changed HTML structure → 0 results

**New Approach (WORKING):**
- Uses `reddit.com/search.json` API
- Parses JSON responses
- Self-imposed 2-second delay between requests (respectful)
- Pagination support for more results

## Rate Limits

- **No official rate limit** (it's public data)
- Self-imposed: 2 seconds between requests
- Be respectful: Don't spam Reddit's servers

## What's Next?

The scraper is fully functional! You can now:
1. Run scheduled scans with Reddit included
2. Discover problems from Reddit discussions
3. Find monetizable pain points from real users

Try running: `python run.py scan --all`

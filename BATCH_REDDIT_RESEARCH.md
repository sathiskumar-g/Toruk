# Batch Reddit Research System

## Quick Start

### 1. Add Your Keywords

Edit `research_keywords.json`:
```json
{
  "reddit_keywords": [
    "I wish there was a tool for context store api",
    "no error handling",
    "difficult to integrate",
    "expensive pricing"
  ]
}
```

### 2. Run Batch Research

```bash
python run.py batch-reddit --limit 10
```

This will:
- Search Reddit for each keyword
- Extract and score problems
- Save individual keyword results
- Create final aggregate report with ALL opportunities

### 3. View Results as Table

```bash
python json_to_table.py data/reddit_research_final_20260117_134631.json
```

Output to file:
```bash
python json_to_table.py data/reddit_research_final_20260117_134631.json -o results.txt
```

Limit rows shown:
```bash
python json_to_table.py data/reddit_research_final_20260117_134631.json --max-rows 20
```

## File Structure

### Individual Keyword Results
Each keyword gets its own file:
```
data/reddit_keyword_I wish there was a tool for_20260117_134303.json
data/reddit_keyword_too expensive_20260117_134537.json
```

### Final Aggregate Report
One file with ALL opportunities ranked:
```
data/reddit_research_final_20260117_134631.json
```

Contains:
- Summary of all keywords processed
- Total opportunities found
- All opportunities ranked by score
- Top 10 opportunities

## Commands

### Single Keyword Search
```bash
python run.py reddit --keyword "I wish there was a tool for" --limit 20
```

### Batch Research (All Keywords)
```bash
python run.py batch-reddit --limit 50
```

Use custom keywords file:
```bash
python run.py batch-reddit --keywords-file my_keywords.json --limit 30
```

### Convert JSON to Table
```bash
# Print to console
python json_to_table.py data/reddit_research_final_20260117.json

# Save to file
python json_to_table.py data/reddit_research_final_20260117.json -o report.txt

# Limit rows
python json_to_table.py data/reddit_research_final_20260117.json --max-rows 15
```

## Understanding the Results

### Keyword Summary Table
Shows performance of each keyword:
- **Posts**: Raw Reddit posts found
- **Problems**: Problems extracted (filtered)
- **Opps**: Opportunities after scoring
- **Top Score**: Best opportunity score for that keyword

### Opportunities Table
Ranked list of all opportunities:
- **Score**: Opportunity score (0-50)
- **Pain**: Pain level (0-10)
- **Engage**: Total engagement (upvotes + comments)
- **Category**: Problem category
- **Recommendation**: Action advice

## Tips

### Good Keywords
✅ "I wish there was a tool for"
✅ "biggest problem with"
✅ "too expensive"
✅ "doesn't work as expected"

### Bad Keywords
❌ Too generic: "problem", "issue"
❌ Too specific: "langchain rate limit on tuesday"

### Optimal Settings
- **limit**: 20-50 per keyword (more = slower)
- **keywords**: 10-20 keywords (more = longer runtime)
- **estimated time**: ~15 seconds per keyword

## Example Workflow

```bash
# 1. Edit keywords
nano research_keywords.json

# 2. Run research
python run.py batch-reddit --limit 30

# 3. View table
python json_to_table.py data/reddit_research_final_*.json

# 4. Save for review
python json_to_table.py data/reddit_research_final_*.json -o results.txt
```

## Output Files

All files saved to `data/` directory:
- `reddit_keyword_*.json` - Individual keyword results
- `reddit_research_final_*.json` - Aggregate report

Timestamp format: `YYYYMMDD_HHMMSS`

## Next Steps

1. Review top opportunities in final report
2. Check engagement scores (higher = more validated pain)
3. Read original Reddit threads for context
4. Prioritize by opportunity score
5. Build solutions for top-scoring problems!

## Advanced Usage

### Search Specific Subreddits
Edit `config.py` → `REDDIT_SUBREDDITS` array

### Adjust Scoring
Edit `processors/scorer.py` → Modify weights

### Add More Keywords
Just edit `research_keywords.json` and run again!

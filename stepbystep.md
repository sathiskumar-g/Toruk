Step-by-Step: How to Use This Tool
Week 1: Research & Discovery
1. Add Your Research Keywords
Edit research_keywords.json:
{
  "reddit_keywords": [
    "I wish there was a tool for",
    "biggest problem with",
    "too expensive",
    "doesn't work as expected",
    "alternative to",
    "hard to integrate",
    "no API for",
    "missing feature",
    "rate limit",
    "documentation is terrible"
  ]
}

2. Run Your Research
⏱️ Takes ~5 minutes for 10 keywords
python run.py batch-reddit --limit 30


3. Review Results
Look for:
python json_to_table.py data/reddit_research_final_*.json


Score 30+ = Strong opportunity
Upvotes 500+ = Many people have this problem
Comments 50+ = Active discussion/validation


Week 1-2: Validation
4. Read Top 10 Opportunities
For each high-scoring opportunity:

a) Click the Reddit URL

Read the original post
Read ALL comments (that's why we fetch them!)
Look for patterns
b) Ask yourself:

Do 5+ people mention the same pain?
Are they frustrated enough to pay?
Is this a recurring problem or one-time?
Can I build a simple solution in 2-4 weeks?

Example from your actual data:


Score: 35.0 | 6,276 upvotes | 342 comments
"Meta just lost $200 billion... expensive AI infrastructure"

→ Opportunity: Build cost-optimization tool for AI APIs
→ Validated: 6K+ upvotes = real pain
→ Actionable: Help people save money on OpenAI/Anthropic calls


5. Deep Dive on Top 3
Pick your top 3 opportunities. For each:
# Search for more related discussions
python run.py reddit --keyword "expensive OpenAI API" --limit 50
python run.py search "openai cost" --limit 50


6. Pick ONE Problem to Solve
Choose based on:

✅ You can build it (2-4 weeks max)
✅ Clear target users (AI developers, SaaS founders, etc.)
✅ They're actively searching (high engagement)
✅ Existing solutions suck (mentioned in comments)
7. Build Simple MVP
Don't build everything! Build the SMALLEST solution that solves the core pain.

Example:

Problem: "OpenAI API too expensive" (Score: 35.0)
MVP: Simple dashboard showing API costs by endpoint + suggestions
Features: Track usage, show costs, suggest cheaper alternatives
NOT included: Complex analytics, team features, integrations (yet!)
8. Share with Problem-Havers
Go back to Reddit threads where people complained:

Post your solution
"Hey, I saw your frustration with X. I built a simple tool that helps with Y. Would love feedback!"
Be helpful, not salesy
Week 3-4: Iterate
9. Get Feedback
People will tell you:

What's missing
What's confusing
What they'd pay for
What competitors do wrong
10. Iterate & Charge
Add most-requested features
Launch on Product Hunt / HN
Start charging ($29-99/mo for B2B tools)
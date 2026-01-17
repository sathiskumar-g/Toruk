"""
Configuration for Problem Research Tool
"""

# Tools/Platforms to monitor for problems
TOOLS_TO_MONITOR = [
    "langchain",
    "n8n", 
    "zapier",
    "make",
    "openai",
    "chatgpt",
    "claude",
    "cursor",
    "copilot",
    "vercel",
    "supabase",
    "firebase",
    "stripe",
    "twilio",
    "anthropic",
    "huggingface",
    "autogen",
    "crewai",
    "flowise",
    "dify",
    "pipedream"
]

# Keywords that indicate problems/complaints
PROBLEM_KEYWORDS = [
    # Frustration
    "frustrated", "frustrating", "annoying", "annoyed",
    "hate", "terrible", "awful", "horrible", "worst",
    
    # Failure
    "broken", "breaks", "broke", "fails", "failed", "failing",
    "doesn't work", "not working", "stopped working",
    "doesn't work as expected", "fails when",
    "error", "bug", "issue", "problem",
    
    # Limitations
    "limitation", "limited", "limitations of", "can't", "cannot", "unable",
    "missing", "lack", "no support", "doesn't support",
    "no memory", "no logs", "hard to debug",
    
    # Cost
    "expensive", "overpriced", "cost too much", "pricing",
    "bill", "charged", "pay too much", "too expensive",
    "rate limit",
    
    # Performance
    "slow", "laggy", "timeout", "throttle",
    "hallucination", "tool calling failed", "automation breaks",
    
    # Complexity
    "confusing", "complicated", "hard to", "difficult",
    "unclear", "documentation", "no docs",
    
    # Requests & Wishes
    "wish", "would be nice", "should have", "need",
    "looking for", "alternative", "replacement",
    "I wish there was a tool for", "why is there no tool",
    "this tool is frustrating", "biggest problem with",
    "alternative to"
]

# Problem categories for classification
CATEGORIES = [
    "debugging",      # Hard to debug, no logs, unclear errors
    "reliability",    # Breaks, fails, inconsistent
    "cost",          # Too expensive, unpredictable billing
    "integration",   # Doesn't work with X, API issues
    "memory",        # Forgets context, no state
    "performance",   # Slow, rate limits
    "documentation", # Bad docs, unclear
    "security",      # Permissions, data concerns
    "scalability",   # Works small, fails at scale
    "ux"            # Confusing, bad interface
]

# GitHub repos to monitor (format: owner/repo)
GITHUB_REPOS = [
    "langchain-ai/langchain",
    "n8n-io/n8n",
    "FlowiseAI/Flowise",
    "langgenius/dify",
    "microsoft/autogen",
    "joaomdmoura/crewAI",
    "supabase/supabase",
    "vercel/next.js"
]

# Subreddits to search (AI, SaaS, automation focus)
REDDIT_SUBREDDITS = [
    "artificial",
    "OpenAI",
    "ChatGPT",
    "LangChain",
    "LocalLLaMA",
    "MachineLearning",
    "learnmachinelearning",
    "SaaS",
    "Entrepreneur",
    "startups",
    "Automate",
    "nocode",
    "automation",
    "webdev",
    "technology",
    "programming",
    "Python",
    "AIAgents",
    "Startup_Ideas",
    "n8n"
]

# Scoring weights for opportunity evaluation
SCORING_WEIGHTS = {
    "pain_intensity": 0.25,
    "market_demand": 0.20,
    "monetization": 0.20,
    "feasibility": 0.20,
    "low_saturation": 0.15  # inverse - lower saturation = higher score
}

# Output paths
DATA_DIR = "data"
OUTPUT_FILES = {
    "hackernews": f"{DATA_DIR}/hackernews_posts.json",
    "github": f"{DATA_DIR}/github_issues.json",
    "extracted": f"{DATA_DIR}/extracted_problems.json",
    "opportunities": f"{DATA_DIR}/opportunities.json"
}

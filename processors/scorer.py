"""
Opportunity Scorer
Scores problems as business opportunities using the "5PM Fit" framework
"""
from typing import List, Dict, Any
from datetime import datetime
import json
import os

# Import config
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SCORING_WEIGHTS


class OpportunityScorer:
    """
    Score problems as business opportunities
    
    Uses the 5PM Fit framework:
    - Pain: How much does it hurt?
    - Pervasiveness: How many people have it?
    - Proximity: Are these your ideal customers?
    - Payment: Will they pay to solve it?
    - Plausibility: Can YOU actually build this?
    """
    
    def __init__(self):
        self.weights = SCORING_WEIGHTS
        self.scored_problems: List[Dict[str, Any]] = []
        
    def score_problems(self, problems: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Score a list of extracted problems
        
        Args:
            problems: List of problem dicts from ProblemExtractor
            
        Returns:
            List of problems with opportunity scores
        """
        print(f"📊 Scoring {len(problems)} problems...")
        
        scored = []
        for problem in problems:
            scored_problem = self._score_problem(problem)
            scored.append(scored_problem)
        
        # Sort by total score
        scored.sort(key=lambda x: x["opportunity_score"]["total"], reverse=True)
        
        self.scored_problems = scored
        print(f"✅ Scored and ranked {len(scored)} opportunities")
        return scored
    
    def _score_problem(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """Score a single problem and add competitor detection"""
        scores = {
            "pain": self._score_pain(problem),
            "pervasiveness": self._score_pervasiveness(problem),
            "proximity": self._score_proximity(problem),
            "payment": self._score_payment(problem),
            "plausibility": self._score_plausibility(problem)
        }
        total = sum(
            scores[key] * self.weights.get(key, 1)
            for key in scores
        ) / sum(self.weights.values())
        problem["opportunity_score"] = {
            **scores,
            "total": round(total, 2)
        }
        problem["recommendation"] = self._get_recommendation(total)
        problem["solution"] = self._generate_solution(problem)
        problem["validation"] = self._generate_validation(problem)
        problem["business"] = self._generate_business_plan(problem)
        problem["roadmap"] = self._generate_roadmap(problem)
        # Add competitor detection
        problem["competitors"] = self._find_competitors(problem)
        return problem

    def _find_competitors(self, problem: Dict[str, Any]) -> list:
        """
        Find competitors: generate a single advanced Google search URL for the problem.
        """
        category = problem.get("category", "")
        keyword = problem.get("research_keyword", "")
        # Use only the research keyword(s) and category for the search
        base_terms = [category, keyword]
        base_terms = [t for t in base_terms if t]
        quoted = ' '.join([f'"{t}"' for t in base_terms])
        operators = ' (alternative OR competitor OR vs OR review OR "similar tool")'
        query = f'{quoted} {operators}'
        url = f'https://www.google.com/search?q={query.replace(" ", "+")}'
        return [{
            "name": "Google Competitor Search",
            "url": url
        }]
    
    def _score_pain(self, problem: Dict[str, Any]) -> float:
        """
        Pain Score (1-10)
        Based on: keywords, language intensity, pain_score from extractor
        """
        base_score = problem.get("pain_score", 5)
        
        # Boost for emotional keywords
        high_pain_keywords = [
            "nightmare", "frustrated", "gave up", "waste", "broken",
            "terrible", "horrible", "awful", "painful", "annoying",
            "hate", "worst", "useless", "disaster", "failing",
            "stuck", "impossible", "ridiculous", "insane", "driving me crazy"
        ]
        text = problem.get("problem_statement", "").lower()
        
        for kw in high_pain_keywords:
            if kw in text:
                base_score += 0.5
        
        return min(base_score, 10)
    
    def _score_pervasiveness(self, problem: Dict[str, Any]) -> float:
        """
        Pervasiveness Score (1-10)
        Based on: engagement, comments, source popularity
        """
        engagement = problem.get("engagement", {})
        reactions = engagement.get("reactions", 0)
        comments = engagement.get("comments", 0)
        
        # Calculate based on engagement
        # 0-5 reactions = 1-3 score
        # 5-20 reactions = 3-5 score
        # 20-50 reactions = 5-7 score
        # 50+ reactions = 7-10 score
        
        if reactions >= 50:
            score = 7 + min((reactions - 50) / 50, 3)
        elif reactions >= 20:
            score = 5 + (reactions - 20) / 15
        elif reactions >= 5:
            score = 3 + (reactions - 5) / 7.5
        else:
            score = 1 + reactions / 2.5
        
        # Boost for high comments
        if comments >= 20:
            score += 1
        elif comments >= 10:
            score += 0.5
        
        return min(round(score, 1), 10)
    
    def _score_proximity(self, problem: Dict[str, Any]) -> float:
        """
        Proximity Score (1-10)
        Are these YOUR target customers?
        
        High proximity for: developers, solopreneurs, small teams
        Lower for: enterprises, non-technical users
        """
        # Default to 7 for developer-focused sources
        source = problem.get("source", "")
        if source in ["hackernews", "github"]:
            return 7.5  # Developer-focused = good proximity
        
        # Check for enterprise indicators (lower proximity for solo dev)
        text = problem.get("problem_statement", "").lower()
        enterprise_words = ["enterprise", "compliance", "sso", "audit", "procurement"]
        
        if any(word in text for word in enterprise_words):
            return 4.0  # Enterprise = harder to sell to
        
        return 6.0  # Default
    
    def _score_payment(self, problem: Dict[str, Any]) -> float:
        """
        Payment Score (1-10)
        Will they pay to solve this?
        
        High payment likelihood:
        - Time-related problems ("hours", "days")
        - Business-critical issues
        - Currently paying for alternatives
        """
        text = problem.get("problem_statement", "").lower()
        
        score = 5.0  # Base score
        
        # Time = Money
        time_words = [
            "hours", "days", "weeks", "wasted time", "spent trying",
            "months", "time consuming", "too long", "slow", "delayed",
            "waiting", "took forever", "time sink", "inefficient", "bottleneck",
            "overdue", "behind schedule", "time sensitive", "urgent", "immediate"
        ]
        if any(word in text for word in time_words):
            score += 2
        
        # Business-critical
        critical_words = [
            "production", "critical", "blocking", "deadline", "clients",
            "downtime", "outage", "emergency", "urgent", "breaking",
            "live site", "customers affected", "business impact", "revenue loss", "mission critical",
            "high priority", "showstopper", "can't ship", "can't deploy", "must fix"
        ]
        if any(word in text for word in critical_words):
            score += 2
        
        # Existing spend (they already pay for something)
        spend_words = [
            "paid", "subscription", "credits", "tokens", "billing",
            "pricing", "expensive", "cost", "budget", "invoice",
            "payment", "charge", "fee", "tier", "plan",
            "enterprise", "premium", "upgrade", "license", "contract"
        ]
        if any(word in text for word in spend_words):
            score += 1
        
        # Category matters
        high_payment_categories = ["API Integration", "Performance", "Configuration"]
        if problem.get("category") in high_payment_categories:
            score += 1
        
        return min(round(score, 1), 10)
    
    def _score_plausibility(self, problem: Dict[str, Any]) -> float:
        """
        Plausibility Score (1-10)
        Can YOU actually build this?
        
        This is subjective - adjust based on your skills.
        Default scoring based on typical solo dev capabilities.
        """
        category = problem.get("category", "")
        
        # Easier to build (solo dev friendly)
        easy_categories = {
            "Documentation": 9,      # Can build tools/guides
            "Configuration": 8,      # Config generators/templates
            "UX/Workflow": 7,        # Better UX wrappers
            "Error Handling": 7,     # Better error messages/tools
            "API Integration": 6,    # Middleware/connectors
        }
        
        # Harder to build
        hard_categories = {
            "Performance": 5,        # Requires deep expertise
            "Authentication": 4,     # Security is tricky
            "Compatibility": 4,      # Version matrix hell
            "Cost/Pricing": 5,       # Need scale to compete
        }
        
        if category in easy_categories:
            return easy_categories[category]
        elif category in hard_categories:
            return hard_categories[category]
        
        return 6.0  # Default
    
    def _generate_solution(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """Generate solution statement and features"""
        category = problem.get("category", "")
        tools = problem.get("tools_mentioned", [])
        statement = problem.get("problem_statement", "")
        
        # Generate solution based on category
        solution_templates = {
            "Documentation": {
                "solution": f"Build an interactive documentation platform with AI-powered search and real-world examples for {', '.join(tools) if tools else 'popular tools'}",
                "mvp": [
                    "Interactive code playground with live examples",
                    "AI-powered semantic search across documentation",
                    "Community-contributed examples and patterns",
                    "Quick-start templates for common use cases",
                    "Visual workflow builder with code generation"
                ],
                "growth": [
                    "Video tutorials and screencasts",
                    "AI code assistant for debugging",
                    "Team collaboration features",
                    "Custom enterprise documentation",
                    "Integration with IDE (VS Code extension)"
                ],
                "value": {
                    "time": "Save 2-5 hours per week on documentation searches",
                    "money": "Reduce support costs by 40% with self-service",
                    "effort": "Cut onboarding time from days to hours"
                }
            },
            "Configuration": {
                "solution": f"Create a visual configuration builder and validator for {', '.join(tools) if tools else 'complex tools'}",
                "mvp": [
                    "Visual configuration builder with drag-and-drop",
                    "Real-time validation and error detection",
                    "Pre-built templates for common setups",
                    "Export to multiple formats (YAML, JSON, ENV)",
                    "Configuration diff and version control"
                ],
                "growth": [
                    "AI-powered configuration optimization",
                    "Team configuration sharing",
                    "Automated environment sync",
                    "Security scanning and compliance checks",
                    "Infrastructure-as-code generation"
                ],
                "value": {
                    "time": "Reduce configuration time from hours to minutes",
                    "money": "Prevent costly production errors ($5k+ per incident)",
                    "effort": "Eliminate trial-and-error configuration"
                }
            },
            "UX/Workflow": {
                "solution": f"Build a better UX layer and workflow automation tool for {', '.join(tools) if tools else 'existing platforms'}",
                "mvp": [
                    "Simplified dashboard with custom views",
                    "One-click workflow templates",
                    "Visual workflow designer",
                    "Smart notifications and alerts",
                    "Keyboard shortcuts and power-user features"
                ],
                "growth": [
                    "AI workflow suggestions",
                    "Multi-tool orchestration",
                    "Team workflow sharing",
                    "Analytics and optimization insights",
                    "Mobile app for on-the-go management"
                ],
                "value": {
                    "time": "Complete workflows 3x faster",
                    "money": "Reduce tool sprawl - consolidate 3-5 tools into one",
                    "effort": "Cut clicks by 70% with smart automation"
                }
            },
            "Error Handling": {
                "solution": f"Create an intelligent error debugging and resolution platform for {', '.join(tools) if tools else 'common tools'}",
                "mvp": [
                    "Error code translator with plain English explanations",
                    "Automated root cause analysis",
                    "Step-by-step fix instructions",
                    "Similar error search and solutions",
                    "One-click apply common fixes"
                ],
                "growth": [
                    "AI-powered debugging assistant",
                    "Proactive error prevention",
                    "Team knowledge base integration",
                    "Automated fix deployment",
                    "Error analytics and trends"
                ],
                "value": {
                    "time": "Resolve errors in minutes instead of hours",
                    "money": "Reduce downtime costs by 60%",
                    "effort": "Eliminate repetitive debugging searches"
                }
            },
            "API Integration": {
                "solution": f"Build an API integration middleware and testing platform for {', '.join(tools) if tools else 'popular APIs'}",
                "mvp": [
                    "Visual API request builder",
                    "Pre-built connectors for popular tools",
                    "Request/response testing sandbox",
                    "Automatic retry and error handling",
                    "Code generation in multiple languages"
                ],
                "growth": [
                    "API monitoring and alerting",
                    "Load testing and performance optimization",
                    "API version management",
                    "Webhook management and debugging",
                    "Enterprise SSO and security"
                ],
                "value": {
                    "time": "Cut integration time from weeks to days",
                    "money": "Save $10k-50k in developer time per integration",
                    "effort": "Reduce integration complexity by 80%"
                }
            },
            "Performance": {
                "solution": f"Create a performance monitoring and optimization tool for {', '.join(tools) if tools else 'applications'}",
                "mvp": [
                    "Real-time performance monitoring",
                    "Bottleneck detection and alerts",
                    "Optimization recommendations",
                    "Before/after performance comparison",
                    "Cost tracking and optimization"
                ],
                "growth": [
                    "AI-powered performance tuning",
                    "Predictive scaling recommendations",
                    "Multi-region performance testing",
                    "Custom performance budgets",
                    "Integration with CI/CD pipelines"
                ],
                "value": {
                    "time": "Identify issues in seconds, not hours",
                    "money": "Reduce infrastructure costs by 30-50%",
                    "effort": "Automate 90% of performance optimization"
                }
            }
        }
        
        # Get template or use default
        template = solution_templates.get(category, {
            "solution": f"Build a specialized tool to solve {category.lower()} problems for {', '.join(tools) if tools else 'developers'}",
            "mvp": [
                "Core problem-solving feature",
                "Simple, clean user interface",
                "Integration with existing workflows",
                "Basic analytics and reporting",
                "Export and sharing capabilities"
            ],
            "growth": [
                "Advanced automation features",
                "Team collaboration tools",
                "API and webhook integrations",
                "Custom branding and white-label",
                "Enterprise security and compliance"
            ],
            "value": {
                "time": "Save 5-10 hours per week",
                "money": "Reduce costs by 30-40%",
                "effort": "Automate 70% of manual work"
            }
        })
        
        return {
            "statement": template["solution"],
            "mvp_features": template["mvp"],
            "growth_features": template["growth"],
            "value_proposition": template["value"]
        }
    
    def _generate_validation(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """Generate market validation metrics"""
        category = problem.get("category", "")
        engagement = problem.get("engagement", {})
        reactions = engagement.get("reactions", 0)
        comments = engagement.get("comments", 0)
        
        # Estimate market size based on category and engagement
        market_size = "Medium"
        if category in ["Documentation", "API Integration", "Configuration"]:
            market_size = "Large (100k+ potential users)"
        elif category in ["UX/Workflow", "Error Handling"]:
            market_size = "Medium (10k-100k potential users)"
        else:
            market_size = "Small (1k-10k potential users)"
        
        # Competition level
        competition = "Medium"
        if category in ["Performance", "Authentication"]:
            competition = "High (many established solutions)"
        elif category in ["Documentation", "Configuration"]:
            competition = "Medium (some solutions exist)"
        else:
            competition = "Low (few specialized solutions)"
        
        # Time to market based on plausibility score
        plausibility = self._score_plausibility(problem)
        if plausibility >= 8:
            timeline = "2-4 weeks (quick MVP)"
        elif plausibility >= 6:
            timeline = "1-2 months (moderate complexity)"
        else:
            timeline = "2-3 months (technical challenges)"
        
        # Risk factors
        risks = []
        if competition == "High (many established solutions)":
            risks.append("High competition - need strong differentiation")
        if category in ["Authentication", "Security"]:
            risks.append("Security critical - requires expertise")
        if reactions < 10:
            risks.append("Lower engagement - validate demand first")
        if category in ["Performance", "Compatibility"]:
            risks.append("Technical complexity - may require specialized skills")
        
        if not risks:
            risks.append("Standard startup risks - validate PMF early")
        
        return {
            "market_size": market_size,
            "competition": competition,
            "time_to_market": timeline,
            "risk_factors": risks,
            "validation_score": round((reactions * 0.6 + comments * 0.4) / 10, 1)
        }
    
    def _generate_business_plan(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """Generate business viability metrics"""
        category = problem.get("category", "")
        payment_score = problem.get("opportunity_score", {}).get("payment", 5)
        
        # Pricing model based on category
        pricing_models = {
            "Documentation": "Freemium + Pro ($19-49/mo)",
            "Configuration": "Usage-based ($0.10/config + Pro plans)",
            "UX/Workflow": "Subscription ($29-99/mo per user)",
            "Error Handling": "Freemium + Credits ($0.01/query)",
            "API Integration": "Subscription ($49-199/mo + usage)",
            "Performance": "Usage-based (% of cost savings)"
        }
        
        pricing = pricing_models.get(category, "Subscription ($29-79/mo)")
        
        # Revenue potential based on payment score and category
        if payment_score >= 8:
            mrr = "$2k-10k MRR (100-200 paying customers)"
            arr = "$24k-120k ARR potential"
        elif payment_score >= 6:
            mrr = "$500-2k MRR (30-80 paying customers)"
            arr = "$6k-24k ARR potential"
        else:
            mrr = "$100-500 MRR (10-30 paying customers)"
            arr = "$1.2k-6k ARR potential"
        
        # Target customers
        customers = {
            "Documentation": ["Developers", "Technical writers", "DevRel teams", "SaaS companies"],
            "Configuration": ["DevOps engineers", "Cloud architects", "Development teams"],
            "UX/Workflow": ["Product managers", "Solopreneurs", "Small dev teams", "Agencies"],
            "Error Handling": ["Junior developers", "Support teams", "QA engineers"],
            "API Integration": ["Backend developers", "Integration specialists", "SaaS companies"],
            "Performance": ["Engineering teams", "CTOs", "FinOps teams"]
        }
        
        target = customers.get(category, ["Developers", "Technical teams", "SaaS companies"])
        
        # Go-to-market strategy
        gtm = f"1) Build in public on Twitter/LinkedIn, 2) Post in {problem.get('source', 'relevant')} communities, 3) SEO for '[tool] tutorial/guide/help', 4) Free tier with viral loop, 5) Partner with tool creators"
        
        return {
            "pricing_model": pricing,
            "monthly_revenue": mrr,
            "annual_revenue": arr,
            "target_customers": target,
            "go_to_market": gtm,
            "unit_economics": {
                "ltv": "$240-1200 (12mo avg retention)",
                "cac": "$50-150 (content + community)",
                "ltv_cac_ratio": "3-8x (healthy)"
            }
        }
    
    def _generate_roadmap(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """Generate phased product roadmap"""
        solution = self._generate_solution(problem)
        
        return {
            "phase_1": {
                "name": "MVP Launch",
                "timeline": "Weeks 1-4",
                "goal": "Validate core value proposition",
                "features": solution["mvp_features"][:3],  # Top 3 MVP features
                "metrics": "50 signups, 10 paying customers, <$500 MRR"
            },
            "phase_2": {
                "name": "Growth",
                "timeline": "Months 2-3",
                "goal": "Scale to profitability",
                "features": solution["mvp_features"][3:] + solution["growth_features"][:2],
                "metrics": "500 users, 50 paying, $2k-5k MRR"
            },
            "phase_3": {
                "name": "Scale",
                "timeline": "Months 4-6",
                "goal": "Product-market fit + expansion",
                "features": solution["growth_features"][2:],
                "metrics": "2k+ users, 200+ paying, $10k+ MRR"
            }
        }
    
    def _get_recommendation(self, score: float) -> str:
        """Get recommendation based on total score"""
        if score >= 35:
            return "\U0001F4B0 WORTH OPPORTUNITY - Worth pursuing immediately"
        elif score >= 30:
            return "\U0001F525 HIGH OPPORTUNITY - Worth pursuing immediately"
        elif score >= 25:
            return "\u2705 GOOD OPPORTUNITY - Worth exploring further"
        elif score >= 20:
            return "\u26A0\uFE0F MODERATE - Needs validation"
        else:
            return "\u274C LOW PRIORITY - Skip for now"
    
    def get_top_opportunities(self, n: int = 10) -> List[Dict[str, Any]]:
        """Get top N opportunities"""
        return self.scored_problems[:n]
    
    def save_opportunities(self, filename: str = None) -> str:
        """Save scored opportunities to JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/opportunities_{timestamp}.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        output = {
            "scored_at": datetime.now().isoformat(),
            "count": len(self.scored_problems),
            "opportunities": self.scored_problems
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved {len(self.scored_problems)} opportunities to {filename}")
        return filename
    
    def print_report(self, top_n: int = 5):
        """Print a summary report of top opportunities"""
        print("\n" + "="*60)
        print("🎯 TOP OPPORTUNITIES REPORT")
        print("="*60)
        
        for i, opp in enumerate(self.scored_problems[:top_n], 1):
            scores = opp["opportunity_score"]
            print(f"\n#{i} [{scores['total']:.1f}/10] {opp['problem_statement'][:50]}...")
            print(f"   📊 Pain: {scores['pain']:.1f} | Pervasive: {scores['pervasiveness']:.1f} | Payment: {scores['payment']:.1f}")
            print(f"   📂 Category: {opp['category']} | Tools: {opp.get('tools_mentioned', [])}")
            print(f"   🔗 {opp['url']}")
            print(f"   {opp['recommendation']}")
        
        print("\n" + "="*60)


# Test
if __name__ == "__main__":
    # Test with sample problems
    sample_problems = [
        {
            "id": "1",
            "source": "hackernews",
            "problem_statement": "LangChain documentation is terrible, spent 3 days trying to get RAG working",
            "category": "Documentation",
            "pain_score": 8,
            "engagement": {"reactions": 45, "comments": 12},
            "tools_mentioned": ["langchain"]
        },
        {
            "id": "2",
            "source": "github",
            "problem_statement": "Memory leak in production after 2 hours with streaming",
            "category": "Performance",
            "pain_score": 9,
            "engagement": {"reactions": 28, "comments": 15},
            "tools_mentioned": ["openai"]
        }
    ]
    
    scorer = OpportunityScorer()
    scored = scorer.score_problems(sample_problems)
    scorer.print_report()

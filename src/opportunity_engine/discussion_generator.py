"""
Generate discussion briefs for opportunities
"""

import logging
import os
from datetime import datetime
from utils.gemini_analyzer import GeminiAnalyzer

logger = logging.getLogger(__name__)

_ROOT = os.path.join(os.path.dirname(__file__), '..', '..')

def generate_briefs(opportunities, research_profile):
    """
    Generate comprehensive briefs for all opportunities
    """

    logger.info("Generating opportunity briefs...")

    analyzer = GeminiAnalyzer()
    briefs = []

    for opp in opportunities:
        logger.info(f"  Generating brief for: {opp['bottleneck']['industry']}")

        # Generate brief with Gemini
        brief = analyzer.generate_opportunity_brief(
            bottleneck=opp['bottleneck'],
            patent_landscape=opp['bottleneck']['patent_status'],
            companies=opp['companies'],
            capabilities=research_profile
        )

        if brief:
            # Save to file
            filename = os.path.join(_ROOT, f"data/opportunities/{opp['bottleneck']['industry']}_{datetime.now().strftime('%Y%m%d')}.md")
            os.makedirs(os.path.dirname(filename), exist_ok=True)

            with open(filename, 'w') as f:
                f.write(brief)

            briefs.append({
                'title': f"{opp['bottleneck']['industry']} Opportunity",
                'brief_file': filename,
                'priority': calculate_priority(opp),
                'companies': len(opp['companies'])
            })

    return briefs

def calculate_priority(opportunity):
    """
    Calculate priority score for opportunity
    """

    score = 0.0

    # Patent white space
    if opportunity['bottleneck']['patent_status']['white_space']:
        score += 0.3

    # Number of target companies
    score += min(len(opportunity['companies']) * 0.1, 0.3)

    # Bottleneck keywords (urgent language)
    urgent_keywords = ['critical', 'bottleneck', 'limiting', 'challenge']
    if any(kw in opportunity['bottleneck']['description'].lower() for kw in urgent_keywords):
        score += 0.2

    # Industry importance (battery, critical minerals = high)
    important_industries = ['battery', 'lithium', 'critical', 'rare earth']
    if any(ind in opportunity['bottleneck']['industry'].lower() for ind in important_industries):
        score += 0.2

    return min(score, 1.0)

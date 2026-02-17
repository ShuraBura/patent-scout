"""
Match industrial bottlenecks with plasma capabilities
"""

import logging
from utils.gemini_analyzer import GeminiAnalyzer

logger = logging.getLogger(__name__)

def match_bottlenecks_to_capabilities(bottlenecks, research_profile):
    """
    Use Gemini to match bottlenecks with plasma capabilities
    Returns list of matched opportunities with scores
    """

    analyzer = GeminiAnalyzer()
    matches = []

    for bottleneck in bottlenecks:
        logger.info(f"  Matching bottleneck: {bottleneck['industry']}")

        result = analyzer.analyze_bottleneck(bottleneck, research_profile)

        if result['success'] and result['analysis'].get('plasma_applicable'):
            feasibility = result['analysis'].get('technical_feasibility', 0)
            commercial = result['analysis'].get('commercial_potential', 0)

            if feasibility >= 5 and commercial >= 5:
                matches.append({
                    'bottleneck': bottleneck,
                    'analysis': result['analysis'],
                    'combined_score': (feasibility + commercial) / 20.0
                })

    # Sort by combined score
    matches.sort(key=lambda x: x['combined_score'], reverse=True)

    logger.info(f"Found {len(matches)} viable plasma matches")
    return matches

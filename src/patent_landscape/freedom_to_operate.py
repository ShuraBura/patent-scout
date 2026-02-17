"""
Freedom to Operate (FTO) analysis
"""

import logging
from patent_landscape.google_patents_scraper import search_google_patents
from patent_landscape.uspto_fetcher import search_uspto

logger = logging.getLogger(__name__)

def analyze_fto(technology_description, target_market='US'):
    """
    Analyze freedom to operate for a technology
    Returns: dict with FTO analysis
    """

    logger.info(f"Analyzing FTO for: {technology_description[:80]}...")

    blocking_patents = []

    # Search both Google Patents and USPTO
    google_patents = search_google_patents(technology_description)
    uspto_patents = search_uspto(technology_description)

    all_patents = google_patents + uspto_patents

    # Filter for potentially blocking patents
    plasma_relevant = [p for p in all_patents
                       if any(kw in p.get('title', '').lower() or kw in p.get('abstract', '').lower()
                              for kw in ['plasma', 'discharge', 'ionization'])]

    if plasma_relevant:
        blocking_patents = plasma_relevant

    return {
        'technology': technology_description,
        'blocking_patents': blocking_patents,
        'fto_clear': len(blocking_patents) == 0,
        'risk_level': 'HIGH' if len(blocking_patents) > 5 else 'MEDIUM' if len(blocking_patents) > 0 else 'LOW',
        'recommendation': _generate_fto_recommendation(blocking_patents)
    }

def _generate_fto_recommendation(blocking_patents):
    if not blocking_patents:
        return "FTO appears clear - proceed with commercialization"
    elif len(blocking_patents) < 3:
        return "Some patents found - conduct detailed patent review with IP counsel"
    else:
        return "Multiple blocking patents found - seek IP counsel before proceeding"

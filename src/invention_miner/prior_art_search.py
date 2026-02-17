"""
Prior art search before patent filing
"""

import logging
from patent_landscape.google_patents_scraper import search_google_patents

logger = logging.getLogger(__name__)

def check_prior_art(invention_description, cpc_codes=None):
    """
    Check prior art for a potential invention
    Returns: dict with prior art findings
    """

    logger.info(f"Checking prior art for: {invention_description[:80]}...")

    results = {
        'invention': invention_description,
        'prior_art_found': [],
        'white_space': True,
        'recommendation': ''
    }

    # Search Google Patents
    patents = search_google_patents(invention_description, max_results=30)

    if patents:
        results['prior_art_found'] = patents
        results['white_space'] = len(patents) < 3
        results['recommendation'] = (
            "Prior art found - review carefully before filing"
            if patents else
            "No close prior art found - proceed with patent application"
        )
    else:
        results['recommendation'] = "No prior art found - favorable for patent filing"

    logger.info(f"Prior art check complete: {len(patents)} patents found")
    return results

"""
Google Patents scraper for patent landscape analysis
"""

import logging
import requests
from bs4 import BeautifulSoup
import time

logger = logging.getLogger(__name__)

def check_patent_landscape(bottleneck):
    """
    Check if plasma approaches exist for this bottleneck
    """

    logger.info(f"  Checking patent landscape for: {bottleneck['industry']}")

    # Build search query
    search_terms = [
        bottleneck['industry'],
        'plasma',
        'processing'
    ]

    query = ' '.join(search_terms)

    # Search Google Patents
    results = search_google_patents(query)

    # Check if white space (no plasma patents)
    plasma_patents = [r for r in results if 'plasma' in r['title'].lower() or 'plasma' in r.get('abstract', '').lower()]

    return {
        'total_patents': len(results),
        'plasma_patents': len(plasma_patents),
        'white_space': len(plasma_patents) == 0,
        'patents': plasma_patents[:5]  # Top 5
    }

def search_google_patents(query, max_results=20):
    """
    Search Google Patents (public search)
    """

    patents = []

    try:
        # Google Patents public search URL
        url = f"https://patents.google.com/?q={query.replace(' ', '+')}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Parse patent results (basic scraping)
            # Note: Google Patents may require more sophisticated parsing
            patent_elements = soup.find_all('search-result-item', limit=max_results)

            for elem in patent_elements:
                title_elem = elem.find('h3')
                if title_elem:
                    patents.append({
                        'title': title_elem.text.strip(),
                        'abstract': '',  # Would need more detailed parsing
                        'source': 'Google Patents'
                    })

        time.sleep(2)  # Rate limiting

    except Exception as e:
        logger.warning(f"Google Patents search failed: {e}")

    return patents

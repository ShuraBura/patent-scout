"""
USPTO patent data fetcher using public API
"""

import logging
import requests

logger = logging.getLogger(__name__)

USPTO_API_BASE = "https://developer.uspto.gov/ds-api"

def search_uspto(query, max_results=20):
    """
    Search USPTO patent database
    """

    patents = []

    try:
        url = f"{USPTO_API_BASE}/patent/application/search"
        params = {
            'searchText': query,
            'rows': max_results,
            'start': 0
        }

        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            results = data.get('response', {}).get('docs', [])

            for doc in results:
                patents.append({
                    'title': doc.get('patent_title', ''),
                    'number': doc.get('patent_number', ''),
                    'abstract': doc.get('patent_abstract', ''),
                    'source': 'USPTO'
                })

    except Exception as e:
        logger.warning(f"USPTO search failed: {e}")

    return patents

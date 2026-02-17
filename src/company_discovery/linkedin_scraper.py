"""
LinkedIn company discovery (public data only)
"""

import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def search_companies_by_keyword(keyword, max_results=10):
    """
    Search LinkedIn for companies by keyword (public search only)
    Note: LinkedIn heavily restricts scraping; this uses public search pages
    """

    companies = []

    try:
        search_url = f"https://www.linkedin.com/search/results/companies/?keywords={keyword.replace(' ', '%20')}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(search_url, headers=headers, timeout=30)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            company_elements = soup.find_all('span', class_='entity-result__title-text')

            for elem in company_elements[:max_results]:
                name = elem.text.strip()
                if name:
                    companies.append({
                        'name': name,
                        'source': 'LinkedIn',
                        'keyword': keyword
                    })

        else:
            logger.warning(f"LinkedIn returned status {response.status_code} - may require auth")

    except Exception as e:
        logger.warning(f"LinkedIn search failed: {e}")

    return companies

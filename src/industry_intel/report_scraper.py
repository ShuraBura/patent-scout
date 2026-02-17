"""
Scrape industry reports from public sources
"""

import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def scrape_report(url, report_type='generic'):
    """
    Scrape text content from a public report URL
    """

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove scripts and styles
            for tag in soup(['script', 'style', 'nav', 'footer']):
                tag.decompose()

            text = soup.get_text(separator=' ', strip=True)

            return {
                'url': url,
                'type': report_type,
                'text': text[:50000],  # Limit size
                'success': True
            }

    except Exception as e:
        logger.warning(f"Failed to scrape {url}: {e}")

    return {'url': url, 'type': report_type, 'text': '', 'success': False}

def get_usgs_mineral_summaries():
    """
    Fetch USGS Mineral Commodity Summaries (public domain)
    """

    url = 'https://www.usgs.gov/centers/nmic/mineral-commodity-summaries'
    return scrape_report(url, report_type='USGS')

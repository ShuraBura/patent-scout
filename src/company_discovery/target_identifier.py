"""
Find target companies that need plasma solutions
"""

import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def find_target_companies(bottleneck):
    """
    Find companies working on this problem but not using plasma
    """

    logger.info(f"  Finding target companies for: {bottleneck['industry']}")

    companies = []

    # Search LinkedIn for companies in this industry
    linkedin_companies = search_linkedin_companies(bottleneck['industry'])

    # Search for companies via web search
    web_companies = search_web_for_companies(bottleneck)

    companies.extend(linkedin_companies)
    companies.extend(web_companies)

    # Deduplicate
    unique_companies = []
    seen_names = set()

    for c in companies:
        if c['name'] not in seen_names:
            unique_companies.append(c)
            seen_names.add(c['name'])

    return unique_companies[:10]  # Top 10

def search_linkedin_companies(industry):
    """
    Search LinkedIn for companies (public profiles only)
    """

    companies = []

    # Note: LinkedIn requires authentication for full access
    # This is a simplified version using public search

    try:
        # LinkedIn public company search
        search_url = f"https://www.linkedin.com/search/results/companies/?keywords={industry.replace(' ', '%20')}"

        headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        response = requests.get(search_url, headers=headers, timeout=30)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Parse company names (simplified)
            # Real implementation would need more sophisticated parsing
            company_elements = soup.find_all('span', class_='entity-result__title-text')

            for elem in company_elements[:5]:
                companies.append({
                    'name': elem.text.strip(),
                    'source': 'LinkedIn',
                    'industry': industry
                })

    except Exception as e:
        logger.warning(f"LinkedIn search failed: {e}")

    return companies

def search_web_for_companies(bottleneck):
    """
    General web search for companies
    """

    companies = []

    # Hardcoded known companies for specific industries
    # In production, this would use more sophisticated discovery

    known_companies = {
        'battery': [
            {'name': 'Northvolt', 'description': 'Battery manufacturing and recycling'},
            {'name': '6K Energy', 'description': 'Battery materials'},
            {'name': 'Redwood Materials', 'description': 'Battery recycling'}
        ],
        'lithium': [
            {'name': 'Livent', 'description': 'Lithium production'},
            {'name': 'Albemarle', 'description': 'Lithium chemicals'},
            {'name': 'SQM', 'description': 'Lithium from brines'}
        ],
        'recycling': [
            {'name': 'Li-Cycle', 'description': 'Lithium-ion battery recycling'},
            {'name': 'Ascend Elements', 'description': 'Battery material recycling'}
        ]
    }

    industry = bottleneck['industry'].lower()

    for key, company_list in known_companies.items():
        if key in industry:
            companies.extend(company_list)

    return companies

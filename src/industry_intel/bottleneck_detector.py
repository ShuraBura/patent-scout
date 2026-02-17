"""
Detect industrial bottlenecks from reports
"""

import logging
import requests
from bs4 import BeautifulSoup
import re

logger = logging.getLogger(__name__)

BOTTLENECK_KEYWORDS = [
    'energy-intensive',
    'inefficient',
    'slow process',
    'high cost',
    'low yield',
    'separation challenge',
    'requires high temperature',
    'long processing time',
    'environmental impact',
    'safety concerns',
    'bottleneck',
    'limitation',
    'challenge'
]

def scan_industry_bottlenecks(industries_config):
    """
    Scan industry reports for process bottlenecks
    """

    logger.info("Scanning industry reports for bottlenecks...")

    bottlenecks = []

    # Scan DOE reports
    doe_bottlenecks = scan_doe_reports(industries_config)
    bottlenecks.extend(doe_bottlenecks)

    # Scan IEA reports
    iea_bottlenecks = scan_iea_reports(industries_config)
    bottlenecks.extend(iea_bottlenecks)

    logger.info(f"Found {len(bottlenecks)} bottlenecks")

    return bottlenecks

def scan_doe_reports(industries_config):
    """
    Scan DOE critical materials reports
    """

    bottlenecks = []

    # DOE Critical Materials report URLs (public)
    doe_urls = [
        'https://www.energy.gov/cmm/critical-materials-reports',
        'https://www.energy.gov/eere/critical-materials'
    ]

    for url in doe_urls:
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                text = soup.get_text()

                # Find sentences with bottleneck keywords
                sentences = re.split(r'[.!?]+', text)

                for sentence in sentences:
                    if any(keyword in sentence.lower() for keyword in BOTTLENECK_KEYWORDS):
                        # Extract potential bottleneck
                        bottleneck = extract_bottleneck_info(sentence)
                        if bottleneck:
                            bottlenecks.append(bottleneck)

        except Exception as e:
            logger.warning(f"Failed to fetch DOE report: {e}")

    return bottlenecks

def scan_iea_reports(industries_config):
    """
    Scan IEA Critical Minerals Outlook
    """

    bottlenecks = []

    # IEA public reports
    iea_urls = [
        'https://www.iea.org/reports/critical-minerals-outlook-2023'
    ]

    for url in iea_urls:
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                text = soup.get_text()

                sentences = re.split(r'[.!?]+', text)

                for sentence in sentences:
                    if any(keyword in sentence.lower() for keyword in BOTTLENECK_KEYWORDS):
                        bottleneck = extract_bottleneck_info(sentence)
                        if bottleneck:
                            bottlenecks.append(bottleneck)

        except Exception as e:
            logger.warning(f"Failed to fetch IEA report: {e}")

    return bottlenecks

def extract_bottleneck_info(sentence):
    """
    Extract structured bottleneck information from sentence
    """

    # Try to identify industry/process
    industries = ['battery', 'lithium', 'recycling', 'mining', 'refining', 'separation']

    sentence_lower = sentence.lower()

    for industry in industries:
        if industry in sentence_lower:
            return {
                'industry': industry,
                'description': sentence.strip(),
                'source': 'DOE/IEA Report',
                'process': 'extraction/processing'
            }

    return None

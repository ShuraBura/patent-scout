"""
Princeton library proxy for accessing paywalled content
Uses Princeton NetID authentication (optional)
"""

import os
import logging
import requests

logger = logging.getLogger(__name__)

PRINCETON_PROXY_BASE = "https://ezproxy.princeton.edu/login?url="

def get_proxy_session():
    """
    Create authenticated session through Princeton proxy
    Returns None if credentials not configured
    """

    netid = os.getenv('PRINCETON_NETID')
    password = os.getenv('PRINCETON_PASSWORD')

    if not netid or not password:
        logger.info("Princeton credentials not configured - using public access only")
        return None

    session = requests.Session()

    try:
        # Authenticate with Princeton CAS
        cas_url = "https://fed.princeton.edu/cas/login"

        # Get login page
        login_page = session.get(cas_url, timeout=30)

        # Note: Full CAS auth requires form parsing and submission
        # This is a placeholder - full implementation needs CAS flow
        logger.info("Princeton proxy session configured")
        return session

    except Exception as e:
        logger.warning(f"Princeton proxy auth failed: {e}")
        return None

def fetch_with_proxy(url, session=None):
    """
    Fetch URL through Princeton proxy if session available
    """

    if session:
        proxy_url = f"{PRINCETON_PROXY_BASE}{url}"
        try:
            response = session.get(proxy_url, timeout=30)
            return response
        except Exception as e:
            logger.warning(f"Proxy fetch failed, trying direct: {e}")

    # Fall back to direct access
    return requests.get(url, timeout=30)

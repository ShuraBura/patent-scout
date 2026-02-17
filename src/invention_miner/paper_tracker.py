"""
Track recent papers for invention opportunities and prior art
"""

import logging
import requests

logger = logging.getLogger(__name__)

def track_recent_papers(research_profile):
    """
    Find recent papers related to research profile topics
    """

    papers = []

    topics = research_profile.get('current_focus', [])

    for topic in topics:
        topic_papers = search_arxiv(topic)
        papers.extend(topic_papers)

    logger.info(f"Found {len(papers)} recent papers")
    return papers

def search_arxiv(topic, max_results=10):
    """
    Search arXiv for recent papers on topic
    """

    papers = []

    try:
        url = f"http://export.arxiv.org/api/query?search_query=all:{topic.replace(' ', '+')}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"

        response = requests.get(url, timeout=30)

        if response.status_code == 200:
            # Parse Atom XML response
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)

            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            for entry in root.findall('atom:entry', ns):
                title = entry.find('atom:title', ns)
                summary = entry.find('atom:summary', ns)
                published = entry.find('atom:published', ns)

                if title is not None:
                    papers.append({
                        'title': title.text.strip(),
                        'abstract': summary.text.strip() if summary is not None else '',
                        'published': published.text if published is not None else '',
                        'source': 'arXiv',
                        'topic': topic
                    })

    except Exception as e:
        logger.warning(f"arXiv search failed for '{topic}': {e}")

    return papers

"""
Patent Scout Main Orchestrator
Runs monthly industry scans and event-driven checks
"""

import os
import sys
import logging
from datetime import datetime
import yaml

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/patent_scout_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """
    Main entry point for Patent Scout
    """

    logger.info("=" * 60)
    logger.info("PATENT SCOUT - IP & Commercial Intelligence")
    logger.info("=" * 60)

    try:
        # Load configurations
        with open('config/yatom_research_profile.yaml', 'r') as f:
            research_profile = yaml.safe_load(f)

        with open('config/industries.yaml', 'r') as f:
            industries = yaml.safe_load(f)

        logger.info("Configurations loaded successfully")

        # Phase 1: Industry Intelligence Scan
        logger.info("\nPhase 1: Industry Intelligence Scan")
        from industry_intel.bottleneck_detector import scan_industry_bottlenecks
        bottlenecks = scan_industry_bottlenecks(industries)
        logger.info(f"  Found {len(bottlenecks)} potential bottlenecks")

        # Phase 2: Patent Landscape Check
        logger.info("\nPhase 2: Patent Landscape Analysis")
        from patent_landscape.google_patents_scraper import check_patent_landscape
        for bottleneck in bottlenecks:
            patent_status = check_patent_landscape(bottleneck)
            bottleneck['patent_status'] = patent_status

        # Phase 3: Company Discovery
        logger.info("\nPhase 3: Company Discovery")
        from company_discovery.target_identifier import find_target_companies
        opportunities = []
        for bottleneck in bottlenecks:
            if bottleneck['patent_status']['white_space']:
                companies = find_target_companies(bottleneck)
                if companies:
                    opportunities.append({
                        'bottleneck': bottleneck,
                        'companies': companies
                    })

        logger.info(f"  Found {len(opportunities)} commercial opportunities")

        # Phase 4: Opportunity Analysis
        if opportunities:
            logger.info("\nPhase 4: Generating Opportunity Briefs")
            from opportunity_engine.discussion_generator import generate_briefs
            briefs = generate_briefs(opportunities, research_profile)

            # Send email with opportunities
            from utils.email_sender import send_monthly_report
            send_monthly_report(briefs)
            logger.info("  Monthly report sent successfully")

        logger.info("\n" + "=" * 60)
        logger.info("PATENT SCOUT COMPLETE")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Error in Patent Scout: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()

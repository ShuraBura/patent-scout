"""
Email notifications for Patent Scout
"""

import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

logger = logging.getLogger(__name__)

def send_monthly_report(briefs):
    """
    Send monthly industry intelligence report
    """

    recipient = os.getenv('EMAIL_RECIPIENT')
    smtp_user = os.getenv('SMTP_USERNAME')
    smtp_pass = os.getenv('SMTP_PASSWORD')

    if not all([recipient, smtp_user, smtp_pass]):
        logger.warning("Email configuration incomplete - skipping email")
        return

    # Build email content
    subject = f"Patent Scout Monthly Report - {datetime.now().strftime('%B %Y')}"

    body = f"""
PATENT SCOUT MONTHLY REPORT - {datetime.now().strftime('%B %Y')}

COMMERCIAL OPPORTUNITIES DETECTED: {len(briefs)}

"""

    # Sort briefs by priority
    briefs_sorted = sorted(briefs, key=lambda x: x['priority'], reverse=True)

    for i, brief in enumerate(briefs_sorted, 1):
        priority_label = "HIGH" if brief['priority'] > 0.7 else "MEDIUM" if brief['priority'] > 0.5 else "LOW"

        body += f"""
OPPORTUNITY {i}: {brief['title']}
Priority: {priority_label} ({brief['priority']:.2f})
Target Companies: {brief['companies']}
Brief file: {brief['brief_file']}

---
"""

    body += """
Full briefs saved to: data/opportunities/
"""

    # Send email
    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)

        logger.info("Monthly report email sent successfully")

    except Exception as e:
        logger.error(f"Failed to send email: {e}")

"""
Gemini Pro API Integration for Patent Scout
Deep reasoning for patent and commercial analysis
"""

import os
import logging
import json
import google.generativeai as genai

logger = logging.getLogger(__name__)

class GeminiAnalyzer:
    """
    Gemini Pro for IP and commercial intelligence
    """

    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')

        if not api_key:
            logger.warning("GEMINI_API_KEY not configured - analysis disabled")
            self.model = None
        else:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-2.0-pro-exp')
                logger.info("Initialized Gemini Pro for IP and commercial analysis")
            except Exception as e:
                logger.error(f"Gemini initialization failed: {e}")
                self.model = None

    def analyze_bottleneck(self, bottleneck, capabilities):
        """
        Determine if plasma could solve this bottleneck
        """

        if not self.model:
            return {'success': False, 'error': 'Gemini not available'}

        prompt = f"""
Analyze industrial bottleneck for plasma solution potential.

BOTTLENECK:
Industry: {bottleneck['industry']}
Process: {bottleneck['process']}
Problem: {bottleneck['description']}

PLASMA CAPABILITIES AVAILABLE:
{self._format_capabilities(capabilities)}

ANALYSIS REQUIRED:
1. Could plasma solve this bottleneck? (Yes/No/Maybe)
2. Which specific plasma capability would apply?
3. Expected improvement (quantitative if possible)
4. Technical feasibility (0-10 scale)
5. Commercial potential (0-10 scale)
6. Key technical risks

Return as JSON:
{{
  "plasma_applicable": boolean,
  "applicable_capability": "string",
  "expected_improvement": "string with numbers",
  "technical_feasibility": number (0-10),
  "commercial_potential": number (0-10),
  "risks": ["risk1", "risk2"],
  "recommendation": "string"
}}
"""

        try:
            response = self.model.generate_content(prompt)
            # Clean response (remove markdown if present)
            text = response.text.replace('```json', '').replace('```', '').strip()
            result = json.loads(text)
            return {'success': True, 'analysis': result}

        except Exception as e:
            logger.error(f"Gemini analysis failed: {e}")
            return {'success': False, 'error': str(e)}

    def generate_opportunity_brief(self, bottleneck, patent_landscape, companies, capabilities):
        """
        Generate comprehensive opportunity discussion brief
        """

        if not self.model:
            return None

        prompt = f"""
You are an IP and commercialization strategist for a plasma physics researcher.

OPPORTUNITY DETECTED:
Industry: {bottleneck['industry']}
Problem: {bottleneck['description']}
Current method limitations: {bottleneck.get('current_limitations', 'N/A')}

PATENT LANDSCAPE:
{self._format_patent_landscape(patent_landscape)}

TARGET COMPANIES:
{self._format_companies(companies)}

RESEARCHER CAPABILITIES:
{self._format_capabilities(capabilities)}

Generate comprehensive discussion brief (2000-3000 words) with:

1. EXECUTIVE SUMMARY (3-4 sentences)
   - The opportunity
   - Market size
   - Priority level

2. INDUSTRIAL PAIN POINT
   - Current process details
   - Quantitative limitations (time, cost, yield)
   - Why it matters

3. YOUR PLASMA SOLUTION
   - Which capability applies
   - How plasma solves it
   - Expected performance improvement (quantitative)
   - Technical feasibility

4. PATENT LANDSCAPE ANALYSIS
   - Prior art summary
   - White space identified
   - Your novel contributions
   - Freedom to operate status
   - IP strategy recommendation

5. COMMERCIAL OPPORTUNITY
   - Market size and growth
   - Target company analysis (top 3)
   - Partnership vs licensing strategy
   - Revenue potential

6. TECHNICAL DEVELOPMENT PLAN
   - Phase 1: Lab validation (timeline)
   - Phase 2: Pilot design
   - Phase 3: Commercial demo
   - Resource requirements

7. DISCUSSION QUESTIONS
   - Should we pursue?
   - Patent first?
   - Which companies to approach?
   - Resource allocation?

Be quantitative, specific, and commercially focused.
Use markdown formatting with ## headers.
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text

        except Exception as e:
            logger.error(f"Brief generation failed: {e}")
            return None

    def _format_capabilities(self, capabilities):
        """Format capabilities for prompt"""
        lines = []
        for cap in capabilities.get('unique_capabilities', []):
            lines.append(f"- {cap['name']}: {cap['description']}")
        return "\n".join(lines)

    def _format_patent_landscape(self, landscape):
        """Format patent landscape for prompt"""
        return f"Total patents: {landscape.get('total_patents', 0)}\nWhite space: {landscape.get('white_space', False)}"

    def _format_companies(self, companies):
        """Format companies for prompt"""
        lines = []
        for c in companies[:5]:  # Top 5
            lines.append(f"- {c['name']}: {c.get('description', 'N/A')}")
        return "\n".join(lines)

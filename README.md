# Patent Scout

IP & Commercial Intelligence for Plasma Research

## Purpose

Patent Scout monitors industrial bottlenecks, patent landscapes, and commercial opportunities where plasma technology could provide solutions. Part of the autonomous intelligence stack for plasma physics research commercialization.

## Features

- **Invention Miner:** Check prior art before publishing; track recent papers
- **Bottleneck Scout:** Find industrial pain points plasma can solve (DOE/IEA/USGS reports)
- **Patent Landscape:** Track IP white space by CPC code and industry
- **Company Discovery:** Identify potential customers and partners
- **Opportunity Briefs:** Generate comprehensive commercialization reports with Gemini

## Setup

### 1. Configure GitHub Secrets

Go to Settings → Secrets → Actions and add:

| Secret | Required | Description |
|--------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Google AI Studio API key |
| `EMAIL_RECIPIENT` | Yes | Email address for reports |
| `SMTP_USERNAME` | Yes | Gmail address for sending |
| `SMTP_PASSWORD` | Yes | Gmail App Password |
| `PRINCETON_NETID` | No | For library proxy access |
| `PRINCETON_PASSWORD` | No | For library proxy access |

### 2. Configure Research Profile

Edit `config/yatom_research_profile.yaml` with your capabilities and priorities.

### 3. Customize Industries

Edit `config/industries.yaml` to add/remove monitored industries.

## Running

### Automatic (GitHub Actions)

- **Monthly scan:** Runs on the 15th of each month
- **Quarterly patent mining:** Runs quarterly (Jan/Apr/Jul/Oct)
- **Prior art check:** Trigger manually via Actions → Event Prior Art Check

### Manual trigger

```bash
# From repository root
cd src && python main.py
```

### On-demand prior art check

Trigger the `event-prior-art-check` workflow manually with your invention description.

## Cost

$0/year - Uses only free resources:
- Google Patents (public search)
- USPTO public API
- DOE/IEA/USGS public reports
- arXiv API
- Gemini API (free tier)

## Integration

### Sentinel → Scout
When Sentinel detects a paper submission, Scout automatically runs a prior art check.

### Oracle → Scout
When Oracle identifies a commercial opportunity, Scout checks the patent landscape and finds target companies.

## Directory Structure

```
patent-scout/
├── src/                    # Python source
│   ├── main.py             # Orchestrator
│   ├── invention_miner/    # Prior art & paper tracking
│   ├── patent_landscape/   # Patent search & FTO
│   ├── industry_intel/     # Bottleneck detection
│   ├── company_discovery/  # Target company finder
│   ├── opportunity_engine/ # Brief generation
│   └── utils/              # Gemini, email, proxy
├── config/                 # YAML configuration
├── data/                   # Output data (gitignored except .gitkeep)
├── templates/              # Report templates
└── .github/workflows/      # Automation
```

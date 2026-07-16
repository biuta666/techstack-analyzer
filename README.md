# TechStack Analyzer

**Open-source website technology intelligence. Detect CMS, frontend frameworks, infrastructure, analytics, and business tools from any URL.**

Built for developers, marketers, and researchers who need to understand the technology stack behind any website.

## Quick Start

```bash
pip install -r requirements.txt
python api/server.py
```

Open http://localhost:8010/scan?url=example.com

## API

```bash
# Scan a website
curl "http://localhost:8010/scan?url=tesla.com"

# Get HTML report
curl "http://localhost:8010/report?url=tesla.com" > tesla_report.html

# Health check
curl "http://localhost:8010/health"
```

## Features

- **60+ fingerprints** across 6 categories
- **HTML scanner** — page content, scripts, meta
- **Header scanner** — server, cookies, powered-by
- **DNS scanner** — IP, nameservers, MX records
- **Confidence scoring** — weighted match system
- **HTML report** — professional technology intelligence

## Supported Detections

| Category | Examples |
|----------|----------|
| CMS | WordPress, Shopify, Webflow, Ghost |
| Frontend | React, Next.js, Vue, Angular, Svelte |
| Backend | Node.js, Django, Rails, Laravel |
| Infrastructure | Cloudflare, AWS, Vercel, Netlify |
| Analytics | GA4, Hotjar, Mixpanel, Plausible |
| Business | Stripe, HubSpot, Intercom, Sentry |

## Architecture

```
URL Input
    ↓
Scanner Engine ─── HTML / Headers / DNS
    ↓
Fingerprint Engine (60+ fingerprints)
    ↓
Technology Intelligence Report
```

## Tech Stack

- Python 3.11, FastAPI
- BeautifulSoup, httpx, dnspython
- SQLite (for future persistence)

## Roadmap

- [x] Basic scanner engine
- [x] Fingerprint detection (60+ patterns)
- [x] HTML report generation
- [ ] Technology change tracking
- [ ] Competitive comparison
- [ ] API key authentication

---

**GitHub**: [github.com/biuta666/techstack-analyzer](https://github.com/biuta666/techstack-analyzer)
**Enterprise**: ieqqnet@163.com

*Built by [biuta666](https://github.com/biuta666)*

"""TechStack Analyzer API - FastAPI server."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

from scanner.html_scanner import scan as html_scan
from scanner.header_scanner import scan as header_scan
from scanner.dns_scanner import scan as dns_scan
from detector.fingerprint_engine import detect
from report.generator import generate_report

app = FastAPI(title="TechStack Analyzer", version="1.0.0", docs_url="/docs")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/")
def root():
    return {
        "name": "TechStack Analyzer",
        "version": "1.0.0",
        "usage": "GET /scan?url=example.com",
        "github": "https://github.com/biuta666/techstack-analyzer",
    }


@app.get("/scan")
def scan_url(url: str):
    """Scan a URL and return detected technologies."""
    if not url:
        return {"error": "url parameter required"}

    # Run all scanners
    html_data = html_scan(url)
    header_data = header_scan(url)
    dns_data = dns_scan(url)

    if html_data.get("error") and header_data.get("error"):
        return {"error": f"Cannot reach {url}: {html_data.get('error')}", "url": url}

    # Detect technologies
    technologies = detect(
        html=html_data.get("html", ""),
        headers=header_data.get("headers", {}),
        scripts=html_data.get("scripts", []),
        dns_info=dns_data,
    )

    return {
        "url": url,
        "domain": url.split("://")[-1].split("/")[0],
        "title": html_data.get("title", ""),
        "status_code": html_data.get("status_code", 0),
        "technologies": technologies,
        "technologies_count": len(technologies),
        "server": header_data.get("server"),
        "powered_by": header_data.get("powered_by"),
        "ip": dns_data.get("ip"),
    }


@app.get("/report")
def get_report(url: str):
    """Generate an HTML technology intelligence report."""
    if not url:
        return HTMLResponse("url parameter required", status_code=400)

    scan_result = scan_url(url)
    if "error" in scan_result:
        return HTMLResponse(f"<h2>Error</h2><p>{scan_result['error']}</p>", status_code=400)

    html_report = generate_report(url, scan_result.get("technologies", []), scan_result)
    return HTMLResponse(content=html_report, status_code=200)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "techstack-analyzer",
        "version": "1.0.0",
        "fingerprints_loaded": len(__import__("detector.fingerprint_engine", fromlist=[""]).load_fingerprints()),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)

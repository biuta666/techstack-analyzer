"""TechStack Analyzer v2.0 - powered by Wappalyzer (7,245 fingerprints)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

from scanner.wappalyzer_scanner import scan as wappalyzer_scan, get_fingerprint_stats
from scanner.html_scanner import scan as html_scan
from scanner.dns_scanner import scan as dns_scan
from report.generator import generate_report
from detector.fingerprint_engine import load_fingerprints

app = FastAPI(title="TechStack Analyzer", version="2.0.0", docs_url="/docs")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/")
def root():
    stats = get_fingerprint_stats()
    return {
        "name": "TechStack Analyzer",
        "version": "2.0.0",
        "fingerprints": stats["total_technologies"],
        "categories": stats["total_categories"],
        "usage": "GET /scan?url=example.com",
        "github": "https://github.com/biuta666/techstack-analyzer",
    }


@app.get("/scan")
def scan_url(url: str):
    """Scan a URL using Wappalyzer's 7,245 fingerprint engine."""
    if not url:
        return {"error": "url parameter required"}

    # Primary: Wappalyzer scan (7,245 fingerprints)
    result = wappalyzer_scan(url)

    # Fallback: custom HTML/DNS scan for metadata
    if result.get("error"):
        html_data = html_scan(url)
        header_data = header_scan(url)
        dns_data = dns_scan(url)
        result.update({
            "title": html_data.get("title", ""),
            "status_code": html_data.get("status_code", 0),
            "server": header_data.get("server"),
            "ip": dns_data.get("ip"),
        })
    else:
        html_data = html_scan(url)
        result["title"] = html_data.get("title", "")
        result["status_code"] = html_data.get("status_code", 0)

    return result


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


@app.get("/fingerprints")
def fingerprint_stats():
    """Get stats about the loaded fingerprint database."""
    return get_fingerprint_stats()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "techstack-analyzer",
        "version": "2.0.0",
        "fingerprints_loaded": len(load_fingerprints()),
        "wappalyzer_db": 7245,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)

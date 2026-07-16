"""Header Scanner - analyzes HTTP headers for technology fingerprints."""
import requests


def scan(url: str, timeout: int = 10) -> dict:
    """Fetch HTTP headers and extract technology signals."""
    if not url.startswith("http"):
        url = "https://" + url

    result = {
        "url": url,
        "headers": {},
        "server": None,
        "powered_by": None,
        "cookies": [],
        "status_code": 0,
        "error": None,
    }

    try:
        resp = requests.head(
            url,
            timeout=timeout,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"},
            allow_redirects=True,
        )
        result["status_code"] = resp.status_code
        result["headers"] = dict(resp.headers)
        result["server"] = resp.headers.get("Server")
        result["powered_by"] = resp.headers.get("X-Powered-By")

        if "Set-Cookie" in resp.headers:
            result["cookies"] = [c.strip() for c in resp.headers.get("Set-Cookie", "").split(";") if c.strip()]

        # Also try GET for headers that HEAD might miss
        if not result["server"] and not result["powered_by"]:
            resp2 = requests.get(url, timeout=timeout, stream=True,
                                 headers={"User-Agent": "Mozilla/5.0 Chrome/120.0.0.0"})
            result["headers"] = dict(resp2.headers)
            result["server"] = resp2.headers.get("Server")
            result["powered_by"] = resp2.headers.get("X-Powered-By")

    except requests.Timeout:
        result["error"] = "Timeout"
    except Exception as e:
        result["error"] = str(e)[:100]

    return result

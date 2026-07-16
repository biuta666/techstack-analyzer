"""HTML Scanner - fetches and parses web pages for technology detection."""
import requests
from bs4 import BeautifulSoup


def scan(url: str, timeout: int = 15) -> dict:
    """Fetch HTML content and extract metadata from a URL."""
    if not url.startswith("http"):
        url = "https://" + url

    result = {
        "url": url,
        "title": "",
        "description": "",
        "html": "",
        "scripts": [],
        "meta_tags": {},
        "headers": {},
        "status_code": 0,
        "error": None,
    }

    try:
        resp = requests.get(
            url,
            timeout=timeout,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
            allow_redirects=True,
        )
        result["status_code"] = resp.status_code
        result["headers"] = dict(resp.headers)

        if "text/html" in resp.headers.get("Content-Type", ""):
            soup = BeautifulSoup(resp.text, "html.parser")
            result["html"] = resp.text

            if soup.title:
                result["title"] = soup.title.string or ""

            for meta in soup.find_all("meta"):
                name = meta.get("name", meta.get("property", ""))
                content = meta.get("content", "")
                if name and content:
                    result["meta_tags"][name] = content

            for script in soup.find_all("script"):
                src = script.get("src", "")
                if src:
                    result["scripts"].append(src)

    except requests.Timeout:
        result["error"] = "Timeout"
    except requests.ConnectionError:
        result["error"] = "Connection failed"
    except Exception as e:
        result["error"] = str(e)[:100]

    return result

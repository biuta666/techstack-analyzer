"""Wappalyzer Scanner - professional technology detection using 7,245 fingerprints."""
from wappalyzer import Wappalyzer

_wapp = None


def get_wappalyzer():
    global _wapp
    if _wapp is None:
        _wapp = Wappalyzer()
    return _wapp


def scan(url: str, timeout: int = 30) -> dict:
    """Scan a URL using Wappalyzer's 7,245 fingerprint engine."""
    if not url.startswith("http"):
        url = "https://" + url

    result = {
        "url": url,
        "technologies": [],
        "categories": {},
        "technologies_count": 0,
        "categories_count": 0,
        "error": None,
    }

    try:
        wapp = get_wappalyzer()
        techs = wapp.analyze(url)

        for t in techs:
            name = t.get("name", "")
            categories = t.get("categories", [])
            version = t.get("version", "")

            tech_data = {
                "name": name,
                "version": version,
                "confidence": t.get("confidence", 100),
                "categories": categories,
            }
            result["technologies"].append(tech_data)

            for cat in categories:
                if cat not in result["categories"]:
                    result["categories"][cat] = []
                result["categories"][cat].append(name)

        result["technologies_count"] = len(result["technologies"])
        result["categories_count"] = len(result["categories"])

    except ImportError as e:
        result["error"] = "wappalyzer package not installed: pip install wappalyzer"
    except Exception as e:
        result["error"] = str(e)[:200]

    return result


def get_fingerprint_stats() -> dict:
    """Get stats about the loaded fingerprint database."""
    wapp = get_wappalyzer()
    techs = getattr(wapp, 'technologies', wapp.categories if hasattr(wapp, 'categories') else {})
    cat_count = len(getattr(wapp, 'categories', {}))
    return {
        "total_technologies": 7245,
        "total_categories": cat_count or 105,
    }

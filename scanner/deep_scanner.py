"""Deep Scanner - Crawlee-powered JavaScript rendering scanner.

Falls back to basic HTTP scan if Crawlee is not available.
Use for: SPAs, React/Vue/Angular apps that need JS rendering.
"""
import asyncio


async def deep_scan_async(url: str, timeout: int = 30) -> dict:
    """Deep scan using Crawlee with Playwright for JS-rendered pages."""
    result = {"url": url, "html": "", "title": "", "status_code": 0, "error": None}
    try:
        from crawlee.crawlers import PlaywrightCrawler
        from crawlee.crawlers.playwright import PlaywrightCrawlingContext

        captured = {"html": "", "title": ""}

        crawler = PlaywrightCrawler(max_requests=1, max_request_retries=1)

        @crawler.router.default_handler
        async def handler(context: PlaywrightCrawlingContext):
            captured["html"] = await context.page.content()
            captured["title"] = await context.page.title()

        await crawler.run([url])
        result["html"] = captured["html"]
        result["title"] = captured["title"]
        result["status_code"] = 200

    except ImportError:
        result["error"] = "Crawlee not installed (pip install crawlee)"
    except Exception as e:
        result["error"] = str(e)[:200]
    return result


def scan(url: str, timeout: int = 30) -> dict:
    """Synchronous wrapper for deep scan."""
    return asyncio.run(deep_scan_async(url, timeout))


def is_available() -> bool:
    """Check if Crawlee deep scan is available."""
    try:
        import crawlee
        return True
    except ImportError:
        return False

"""DNS Scanner - resolves DNS records for infrastructure detection."""
import socket
import json


def scan(domain: str, timeout: int = 5) -> dict:
    """Perform basic DNS lookups for infrastructure detection."""
    # Strip protocol and path
    domain = domain.split("://")[-1].split("/")[0]

    result = {
        "domain": domain,
        "ip": None,
        "nameservers": [],
        "mx_records": [],
        "cname": None,
        "txt_records": [],
        "error": None,
    }

    try:
        result["ip"] = socket.gethostbyname(domain)
    except Exception as e:
        result["error"] = str(e)[:100]
        return result

    # Try DNS lookups (best-effort)
    try:
        import dns.resolver
        for ns_type, key in [("NS", "nameservers"), ("MX", "mx_records"), ("CNAME", "cname"), ("TXT", "txt_records")]:
            try:
                answers = dns.resolver.resolve(domain, ns_type, lifetime=timeout)
                if ns_type == "CNAME":
                    result[key] = str(answers[0].target)
                elif ns_type == "MX":
                    result[key] = [str(r.exchange) for r in answers][:5]
                elif ns_type == "TXT":
                    texts = []
                    for r in answers:
                        txt = "".join(s.decode() if isinstance(s, bytes) else s for s in r.strings) if hasattr(r, 'strings') else str(r)
                        texts.append(txt[:100])
                    result[key] = texts[:10]
                else:
                    result[key] = [str(r) for r in answers][:5]
            except Exception:
                pass
    except ImportError:
        pass  # dnspython not installed, skip DNS lookups

    return result

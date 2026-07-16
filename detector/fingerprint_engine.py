"""Fingerprint Engine - matches scan results against technology fingerprints."""
import os, json


FINGERPRINTS_DIR = os.path.join(os.path.dirname(__file__), "fingerprints")


def load_fingerprints() -> list:
    """Load all fingerprint files from the fingerprints directory."""
    all_fingerprints = []
    if not os.path.exists(FINGERPRINTS_DIR):
        return all_fingerprints

    for f in sorted(os.listdir(FINGERPRINTS_DIR)):
        if f.endswith(".json"):
            path = os.path.join(FINGERPRINTS_DIR, f)
            try:
                with open(path, "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                    all_fingerprints.extend(data)
            except (json.JSONDecodeError, IOError):
                pass

    return all_fingerprints


def detect(html: str, headers: dict, scripts: list, dns_info: dict) -> list:
    """Detect technologies from scan results.

    Returns list of detected technologies with confidence scores.
    """
    fingerprints = load_fingerprints()
    detected = []
    seen = set()

    # Build searchable text from all sources
    search_text = (html or "").lower()
    header_text = " ".join(f"{k}: {v}" for k, v in (headers or {}).items()).lower()
    script_text = " ".join(scripts or []).lower()
    dns_text = json.dumps(dns_info or {}).lower()

    combined_text = f"{search_text}\n{header_text}\n{script_text}\n{dns_text}"

    for fp in fingerprints:
        name = fp.get("name", "")
        if name in seen:
            continue

        patterns = fp.get("patterns", [])
        weight = fp.get("weight", 1)
        matches = 0

        for pattern in patterns:
            if pattern.lower() in combined_text:
                matches += 1

        if matches >= weight:
            confidence = min(100, int((matches / max(weight, 1)) * 100))
            detected.append({
                "name": name,
                "category": fp.get("category", "Other"),
                "confidence": confidence,
                "matches": matches,
            })
            seen.add(name)

    # Sort by confidence descending
    detected.sort(key=lambda x: x["confidence"], reverse=True)
    return detected

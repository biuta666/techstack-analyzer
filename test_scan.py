"""Quick test for TechStack Analyzer"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(os.path.dirname(__file__))

from detector.fingerprint_engine import detect, load_fingerprints

# Test 1: Fingerprint loading
fps = load_fingerprints()
print("Fingerprints: %d" % len(fps))
assert len(fps) == 61, "Expected 61 fingerprints"

# Test 2: WordPress detection
html = '<html><head><link rel="stylesheet" href="/wp-content/themes/style.css"><script src="/wp-includes/js/jquery.js"></script></head><body>Hello WordPress site</body></html>'
techs = detect(html, {"server": "nginx"}, ["wp-content", "wp-json"], {})
print("WordPress test: %d techs" % len(techs))
for t in techs:
    print("  %s %d%% [%s]" % (t["name"], t["confidence"], t["category"]))
assert any(t["name"] == "WordPress" for t in techs), "WordPress not detected"

# Test 3: React + Cloudflare
html2 = '<html><head><script src="/static/js/main.js"></script><div id="root"></div></head><body><script>React.createElement("div", null)</script></body></html>'
techs2 = detect(html2, {"server": "cloudflare", "cf-ray": "test"}, ["react"], {})
print("\nReact + Cloudflare test: %d techs" % len(techs2))
for t in techs2:
    print("  %s %d%% [%s]" % (t["name"], t["confidence"], t["category"]))
assert any(t["name"] == "React" for t in techs2), "React not detected"
assert any(t["name"] == "Cloudflare" for t in techs2), "Cloudflare not detected"

# Test 4: Clean test (no false positives)
html3 = "<html><head><title>Test Page</title></head><body><p>Hello world</p></body></html>"
techs3 = detect(html3, {}, [], {})
print("\nClean page test: %d techs (expected 0)" % len(techs3))
assert len(techs3) == 0, "Clean page should have no detections"

print("\nALL TESTS PASS")

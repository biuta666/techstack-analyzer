"""Test Wappalyzer fingerprints integration."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(os.path.dirname(__file__))

from detector.fingerprint_engine import load_fingerprints, detect

fps = load_fingerprints()
print("Fingerprints loaded: %d" % len(fps))
assert len(fps) > 1000, "Should have 1000+ fingerprints"

# Test 1: WordPress + PHP detection
html = '<html><head><link rel="stylesheet" href="wp-content/themes/style.css"><script src="wp-includes/js/jquery.js"></script></head><body><div id="wpadminbar"></div></body></html>'
headers = {"server": "nginx", "x-powered-by": "PHP/8.2"}
techs = detect(html, headers, ["wp-content", "wp-json", "jquery"], {})

print("\nWordPress test: %d technologies" % len(techs))
found_wp = False
for t in techs[:10]:
    print("  %s %d%% [%s]" % (t["name"], t["confidence"], t["category"]))
    if "WordPress" in t["name"] or "PHP" in t["name"]:
        found_wp = True
assert found_wp, "WordPress/PHP should be detected"

# Test 2: Ecommerce detection
html2 = '<html><body><script src="myshopify.com"></script><div class="product-price"></div><form action="/cart"></form></body></html>'
techs2 = detect(html2, {}, ["shopify"], {})
print("\nShopify test: %d technologies" % len(techs2))
for t in techs2[:8]:
    print("  %s %d%% [%s]" % (t["name"], t["confidence"], t["category"]))

# Test 3: React
html3 = '<html><head><script src="/static/js/main.js"></script></head><body><div id="root"></div><script>React.createElement("div", null)</script></body></html>'
techs3 = detect(html3, {"server": "cloudflare"}, ["react", "static"], {})
print("\nReact + Cloudflare test: %d technologies" % len(techs3))
for t in techs3[:8]:
    print("  %s %d%% [%s]" % (t["name"], t["confidence"], t["category"]))

print("\nALL WAPPALYZER INTEGRATION TESTS PASS")

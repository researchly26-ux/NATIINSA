"""
NatIvyberNotes — IP Classifier + Geolocation Backend
=====================================================
Install:  pip install flask flask-cors requests
Run:      python app.py
Open:     http://127.0.0.1:5000

Free GeoIP API: ipwho.is  (HTTPS, no key, no signup)
Alternative:    ipapi.co   (HTTPS, 1000/day free)
"""

# Standard library
import os

# Third-party (install with: pip install flask flask-cors requests)
from flask import Flask, request, jsonify, send_from_directory  # type: ignore
from flask_cors import CORS                                      # type: ignore
import requests as http                                          # type: ignore


# ── App setup ────────────────────────────────────────────────────────────────
app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)


# ── Helper ───────────────────────────────────────────────────────────────────
def parse_ipv4(raw: str):
    """Return (octets_list, None) on success or (None, error_str) on failure."""
    ip = raw.strip()
    parts = ip.split(".")
    if len(parts) != 4:
        return None, "Invalid format — use IPv4, e.g. 8.8.8.8"
    octets = []
    for p in parts:
        if not p.isdigit():
            return None, f'Bad octet "{p}" — must be a number'
        n = int(p)
        if not 0 <= n <= 255:
            return None, f"Octet {n} out of range — must be 0-255"
        octets.append(n)
    return octets, None


def is_private(octets):
    a, b = octets[0], octets[1]
    return (
        a == 10
        or (a == 172 and 16 <= b <= 31)
        or (a == 192 and b == 168)
        or a == 127
    )


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def serve_index():
    """Serve the frontend so http://127.0.0.1:5000 opens the site."""
    return send_from_directory(".", "index.html")


@app.route("/classify", methods=["POST"])
def classify():
    """
    POST /classify
    Body: { "ip": "192.168.1.1" }
    Returns IP class, subnet mask, description, and whether it's private.
    """
    body = request.get_json(silent=True)
    if not body or "ip" not in body:
        return jsonify({"success": False, "error": 'Missing "ip" in request body'}), 400

    octets, err = parse_ipv4(body["ip"])
    if err:
        return jsonify({"success": False, "error": err}), 400

    ip = ".".join(str(o) for o in octets)
    first = octets[0]

    CLASS_TABLE = {
        "invalid":  (0,   0,   "Invalid (0.x.x.x)", "N/A",                "N/A",  "Reserved — 0.0.0.0 is used before DHCP assigns an address. Not routable."),
        "a":        (1,   126, "Class A",            "255.0.0.0",           "24",  "Very large networks. 8 network bits, 24 host bits — up to 16 million hosts per network."),
        "loopback": (127, 127, "Loopback",            "255.0.0.0",           "24",  "Reserved for localhost (127.0.0.1). Packets never leave the machine."),
        "b":        (128, 191, "Class B",            "255.255.0.0",         "16",  "Medium networks. 16 network bits, 16 host bits — up to 65,534 hosts per network."),
        "c":        (192, 223, "Class C",            "255.255.255.0",        "8",  "Small networks. 24 network bits, 8 host bits — up to 254 hosts. Most common class."),
        "d":        (224, 239, "Class D",            "N/A (Multicast)",    "N/A",  "Reserved for multicast groups (e.g. OSPF, video streaming). Not assigned to hosts."),
        "e":        (240, 255, "Class E",            "N/A (Experimental)", "N/A",  "Reserved by IANA for experimental use. Never used in production."),
    }

    for key, (lo, hi, label, subnet, bits, desc) in CLASS_TABLE.items():
        if lo <= first <= hi:
            return jsonify({
                "success":     True,
                "ip":          ip,
                "class":       label,
                "subnet_mask": subnet,
                "host_bits":   bits,
                "description": desc,
                "is_private":  is_private(octets),
            })

    return jsonify({"success": False, "error": "Unrecognised IP range"}), 400


@app.route("/geolocate", methods=["GET"])
def geolocate():
    """
    GET /geolocate?ip=8.8.8.8

    Uses ipwho.is — completely FREE, HTTPS, no API key.
    Falls back to ipapi.co  — free 1,000 req/day, HTTPS, no key.
    """
    ip_raw = request.args.get("ip", "").strip()
    if not ip_raw:
        return jsonify({"success": False, "error": 'Pass ?ip=x.x.x.x'}), 400

    octets, err = parse_ipv4(ip_raw)
    if err:
        return jsonify({"success": False, "error": err}), 400

    ip = ".".join(str(o) for o in octets)

    if is_private(octets):
        return jsonify({
            "success":    False,
            "is_private": True,
            "error":      "Geolocation not available for private / loopback addresses.",
        })

    # ── Primary: ipwho.is (HTTPS, free, no key needed) ──────────────────────
    try:
        r = http.get(f"https://ipwho.is/{ip}", timeout=6)
        d = r.json()
        if d.get("success") is not False:
            return jsonify({
                "success":      True,
                "ip":           ip,
                "country":      d.get("country"),
                "country_code": d.get("country_code"),
                "flag":         (d.get("flag") or {}).get("emoji", ""),
                "region":       d.get("region"),
                "city":         d.get("city"),
                "postal":       d.get("postal"),
                "latitude":     d.get("latitude"),
                "longitude":    d.get("longitude"),
                "timezone":     (d.get("timezone") or {}).get("id"),
                "isp":          (d.get("connection") or {}).get("isp") or d.get("org"),
                "asn":          f'AS{(d.get("connection") or {}).get("asn", "")}',
                "source":       "ipwho.is",
            })
    except Exception:
        pass  # fall through to backup

    # ── Fallback: ipapi.co (HTTPS, 1,000/day free, no key) ──────────────────
    try:
        r2 = http.get(f"https://ipapi.co/{ip}/json/", timeout=6)
        d2 = r2.json()
        if not d2.get("error"):
            return jsonify({
                "success":      True,
                "ip":           ip,
                "country":      d2.get("country_name"),
                "country_code": d2.get("country_code"),
                "flag":         "",
                "region":       d2.get("region"),
                "city":         d2.get("city"),
                "postal":       d2.get("postal"),
                "latitude":     d2.get("latitude"),
                "longitude":    d2.get("longitude"),
                "timezone":     d2.get("timezone"),
                "isp":          d2.get("org"),
                "asn":          d2.get("asn"),
                "source":       "ipapi.co",
            })
        raise ValueError(d2.get("reason", "ipapi.co error"))
    except Exception as e:
        return jsonify({"success": False, "error": f"Both geo APIs failed: {e}"}), 503


@app.route("/myip", methods=["GET"])
def my_ip():
    """GET /myip — returns caller's public IP address."""
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    return jsonify({"success": True, "ip": ip.split(",")[0].strip()})


# ── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 52)
    print("  NatIvyberNotes — IP Classifier + Geo Backend")
    print("  Install: pip install flask flask-cors requests")
    print("=" * 52)
    print("  Endpoints:")
    print("    GET  /                → opens index.html")
    print("    POST /classify        → classify an IPv4")
    print("    GET  /geolocate?ip=.. → free HTTPS geoloc")
    print("    GET  /myip            → your public IP")
    print("=" * 52)
    print("  GeoIP APIs (both FREE, HTTPS, no key):")
    print("    Primary:  https://ipwho.is/{ip}")
    print("    Fallback: https://ipapi.co/{ip}/json/")
    print("=" * 52)
    app.run(host="127.0.0.1", port=5000, debug=True)

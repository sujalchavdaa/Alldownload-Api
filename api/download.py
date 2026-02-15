from flask import Flask, request, jsonify
import requests, re

app = Flask(__name__)

TARGET_URL = "https://mysocialdownloader.com/wp-admin/admin-ajax.php"

BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://mysocialdownloader.com",
    "Referer": "https://mysocialdownloader.com/",
}

def fetch_nonce(session: requests.Session) -> str | None:
    # Homepage (ya relevant page) se nonce dhundho
    r = session.get("https://mysocialdownloader.com/", headers=BASE_HEADERS, timeout=30)
    text = r.text

    # Common patterns (site ke hisaab se match badal sakta hai)
    patterns = [
        r'nonce"\s*:\s*"([a-zA-Z0-9]+)"',
        r"nonce'\s*:\s*'([a-zA-Z0-9]+)'",
        r'data-nonce="([a-zA-Z0-9]+)"',
        r'"nonce"\s*=\s*"([a-zA-Z0-9]+)"',
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return m.group(1)
    return None

@app.route("/api/download", methods=["GET"])
def download():
    video_url = request.args.get("url")
    if not video_url:
        return jsonify({"status": False, "error": "URL parameter missing"}), 400

    with requests.Session() as s:
        try:
            nonce = fetch_nonce(s)
            if not nonce:
                return jsonify({"status": False, "error": "Nonce fetch failed (site changed/blocked)"}), 400

            payload = {
                "action": "sdl_process_download",
                "nonce": nonce,
                "url": video_url,
                "platform": "instagram"
            }

            r = s.post(TARGET_URL, data=payload, headers=BASE_HEADERS, timeout=30)

            # Kabhi-kabhi JSON nahi aata (HTML / block page)
            try:
                raw_json = r.json()
            except Exception:
                return jsonify({
                    "status": False,
                    "error": "Non-JSON response (possible block)",
                    "http_status": r.status_code,
                    "body_preview": r.text[:300]
                }), 400

            if not raw_json.get("success"):
                return jsonify({
                    "status": False,
                    "error": raw_json.get("data") or raw_json
                }), 400

            inner = raw_json.get("data", {})
            return jsonify({
                "status": True,
                "platform": inner.get("platform"),
                "title": inner.get("title"),
                "thumbnail": inner.get("thumbnail"),
                "download_url": inner.get("download_url"),
                "formats": inner.get("formats"),
                "remaining_downloads": inner.get("remaining_downloads")
            })

        except Exception as e:
            return jsonify({"status": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)

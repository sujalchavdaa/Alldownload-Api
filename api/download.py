from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TARGET_URL = "https://mysocialdownloader.com/wp-admin/admin-ajax.php"
NONCE = "eb0f24e713"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://mysocialdownloader.com",
    "Referer": "https://mysocialdownloader.com/"
}

@app.route("/api/download", methods=["GET"])
def download():
    video_url = request.args.get("url")

    if not video_url:
        return jsonify({"status": False, "error": "URL parameter missing"}), 400

    payload = {
        "action": "sdl_process_download",
        "nonce": NONCE,
        "url": video_url,
        "platform": "instagram"
    }

    try:
        r = requests.post(TARGET_URL, data=payload, headers=HEADERS, timeout=30)
        raw_json = r.json()

        if not raw_json.get("success"):
            return jsonify({"status": False, "error": "Download failed"}), 400

        inner_data = raw_json.get("data")

        return jsonify({
            "status": True,
            "platform": inner_data.get("platform"),
            "title": inner_data.get("title"),
            "thumbnail": inner_data.get("thumbnail"),
            "download_url": inner_data.get("download_url"),
            "formats": inner_data.get("formats"),
            "remaining_downloads": inner_data.get("remaining_downloads")
        })

    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500


# This is required for Vercel
def handler(request):
    return app(request.environ, start_response)

# 🚀 AllDownload API

A simple Flask-based API for downloading videos from supported platforms (YouTube, Instagram, etc).

---

## 🌍 Live API

https://alldownload-api.vercel.app/api/download?url=VIDEO_URL

### Example

https://alldownload-api.vercel.app/api/download?url=https://youtu.be/-j0rjlfmDx4

---

## 📦 Response Format

{
  "status": true,
  "platform": "youtube",
  "title": "Video Title",
  "thumbnail": "Thumbnail URL",
  "download_url": "Best Quality URL",
  "formats": [
    {
      "quality": "360p",
      "ext": "mp4",
      "url": "Download URL"
    },
    {
      "quality": "720p",
      "ext": "mp4",
      "url": "Download URL"
    }
  ],
  "remaining_downloads": {
    "youtube": 10,
    "other": 20
  }
}

---

## 🛠 Run Locally

1. Install Dependencies

pip install -r requirements.txt

2. Start Server

cd api
py index.py

3. Open in Browser

http://127.0.0.1:5000/api/download?url=VIDEO_URL

---

## 📂 Project Structure

api/
  index.py
requirements.txt
vercel.json
README.md

---

## 🌐 Deploy on Vercel

1. Push project to GitHub
2. Import repository into Vercel
3. Click Deploy

---

## ⚠️ Disclaimer

This project is for educational purposes only.

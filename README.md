# Video Extractor API

## Overview
A REST API for extracting the original video URL and metadata from a given video link on any supported platform (TikTok, YouTube, Instagram, Facebook, Twitter/X, Vimeo, and more) using yt-dlp.

## How the API Works
- **Input:** A video URL sent via a `POST` request to the `/extract` endpoint.
- **Processing:** The URL is analyzed using yt-dlp to extract available metadata.
- **Output:** JSON containing video ID, title, uploader name, thumbnail, description, list of formats with direct URLs, and the best quality direct link (`best_url`).

## Example Request
```
curl -X POST http://localhost:5000/extract \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.tiktok.com/@scout2015/video/6718335390845095173"}'
```

## Example Response
```json
{
  "ok": true,
  "data": {
    "id": "6718335390845095173",
    "title": "Example title",
    "uploader": "scout2015",
    "thumbnail": "https://...jpg",
    "best_url": "https://...mp4",
    "formats": [
      {
        "format_id": "720p",
        "ext": "mp4",
        "url": "https://...mp4"
      }
    ]
  }
}
```

## Running Locally
1. Create a virtual environment:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
2. Run the app:
```
python app.py
```

## Using Docker
```
docker build -t video-extractor .
docker run -p 5000:5000 video-extractor
```

## Notes
- Some platforms return temporary signed URLs.
- Respect copyright laws and each platform's terms of service.
- For production, add authentication, rate limiting, and caching.

# ---------- optional: simple test (test_extract.py) ----------
import requests

def test():
    url = 'http://localhost:5000/extract'
    r = requests.post(url, json={'url': 'https://www.tiktok.com/@scout2015/video/6718335390845095173'})
    print(r.json())

if __name__ == '__main__':
    test()
    

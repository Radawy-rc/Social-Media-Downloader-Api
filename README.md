This API extracts original video URLs and metadata from a given video link. It uses yt-dlp so it supports TikTok, YouTube, Instagram, Twitter/X, Facebook, Vimeo and many others.

## Endpoints
POST /extract
JSON body: { "url": "<video_url>" }

Response: { "ok": true, "data": { ... } }

`data` includes: id, title, uploader, thumbnail, description, formats (list), best_url (best direct media URL).

## Run locally
1. python -m venv venv && source venv/bin/activate
2. pip install -r requirements.txt
3. python app.py

## Docker
docker build -t video-extractor .
docker run -p 5000:5000 video-extractor

## Example
curl -X POST http://localhost:5000/extract -H "Content-Type: application/json" -d '{"url":"https://www.tiktok.com/@scout2015/video/6718335390845095173"}'

## Notes and caveats
- yt-dlp respects site access methods. Some platforms block direct access or return signed urls that expire. `best_url` might be time-limited.
- Make sure you comply with copyright and platform ToS when downloading content.
- For production add rate limiting, authentication, logging, and caching.

# ---------- optional: simple test (test_extract.py) ----------
import requests

def test():
    url = 'http://localhost:5000/extract'
    r = requests.post(url, json={'url': 'https://www.tiktok.com/@scout2015/video/6718335390845095173'})
    print(r.json())

if __name__ == '__main__':
    test()
    

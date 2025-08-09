# Project: video_extractor_api
# Files included below. Save each section to its filename.

# ---------- app.py ----------
from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL
import logging
import validators

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

YTDLP_OPTS = {
    'quiet': True,
    'no_warnings': True,
    'skip_download': True,
    'forcejson': True,
}

def extract(url: str):
    if not validators.url(url):
        raise ValueError('invalid_url')
    with YoutubeDL(YTDLP_OPTS) as ydl:
        info = ydl.extract_info(url, download=False)
    # Normalize common fields
    result = {
        'id': info.get('id'),
        'title': info.get('title'),
        'uploader': info.get('uploader') or info.get('creator') or info.get('channel'),
        'uploader_id': info.get('uploader_id'),
        'upload_date': info.get('upload_date'),
        'duration': info.get('duration'),
        'view_count': info.get('view_count'),
        'like_count': info.get('like_count'),
        'thumbnail': info.get('thumbnail'),
        'description': info.get('description'),
        'webpage_url': info.get('webpage_url'),
        'extractor': info.get('extractor'),
        'formats': [],
    }
    formats = info.get('formats') or []
    for f in formats:
        # Keep useful fields only
        result['formats'].append({
            'format_id': f.get('format_id'),
            'ext': f.get('ext'),
            'filesize': f.get('filesize') or f.get('filesize_approx'),
            'width': f.get('width'),
            'height': f.get('height'),
            'tbr': f.get('tbr'),
            'url': f.get('url'),
            'protocol': f.get('protocol'),
        })
    # attempt to pick best direct video url
    best_url = None
    # prefer formats that contain both audio+video
    for f in reversed(result['formats']):
        if f['url']:
            best_url = f['url']
            break
    result['best_url'] = best_url
    return result


@app.route('/extract', methods=['POST'])
def api_extract():
    body = request.get_json(force=True)
    url = body.get('url') if body else None
    if not url:
        return jsonify({'error': 'url_required'}), 400
    try:
        data = extract(url)
        return jsonify({'ok': True, 'data': data})
    except ValueError as e:
        return jsonify({'ok': False, 'error': str(e)}), 400
    except Exception as e:
        logging.exception('extract failed')
        return jsonify({'ok': False, 'error': 'internal_error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

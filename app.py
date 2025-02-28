from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    format = request.args.get('format', 'mp3')

    if not url:
        return jsonify({"error": "URL is required"}), 400

    ydl_opts = {
        'format': 'bestaudio/best' if format == 'mp3' else 'best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if format == 'mp3' else []
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return jsonify({"title": info['title'], "url": info['url']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

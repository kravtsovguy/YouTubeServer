from flask import Flask
from flask import jsonify
from flask import request
import os
import json
import youtube_dl

app = Flask(__name__)
allow_formats = ['22', '18', '36', '17']

@app.route("/info/<video_id>",  methods=['GET'])
def get_urls(video_id):
	info = {}
	urls = {}

	with youtube_dl.YoutubeDL({}) as ydl:
		result = ydl.extract_info('https://www.youtube.com/watch?v={}&hl=ru_RU'.format(video_id), download=False)
		formats = result['formats']

	for f in formats:
		format_id = f['format_id']
		if format_id in allow_formats:
			urls[format_id] = f['url']

	info['id'] = result['id']
	info['title'] = result['title']
	info['author'] = result['uploader']
	info['length_seconds'] = result['duration']
	info['thumbnail_small'] = 'https://i.ytimg.com/vi/{}/default.jpg'.format(info['id'])
	info['thumbnail_large'] = 'https://i.ytimg.com/vi/{}/hqdefault.jpg'.format(info['id'])
	info['urls'] = urls

	return jsonify(info)

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)

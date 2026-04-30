from flask import Flask, request, jsonify
import subprocess
import os
import requests
import tempfile

app = Flask(_name_)

@app.route('/render', methods=['POST'])
def render():
    data = request.json
    video_url = data.get('video_url')
    audio_url = data.get('audio_url')
    output_path = '/tmp/output.mp4'
    video_path = '/tmp/video.mp4'
    audio_path = '/tmp/audio.mp3'
    
    r = requests.get(video_url)
    with open(video_path, 'wb') as f:
        f.write(r.content)
    
    r = requests.get(audio_url)
    with open(audio_path, 'wb') as f:
        f.write(r.content)
    
    subprocess.run(['ffmpeg', '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'aac', '-shortest', output_path, '-y'])
    
    return jsonify({'status': 'done', 'file': output_path})

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

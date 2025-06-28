from flask import Flask, render_template, request, send_from_directory
import os
from pytube import YouTube
import requests

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    filename = ''
    if request.method == 'POST':
        url = request.form['url']
        try:
            if 'youtube.com' in url or 'youtu.be' in url:
                yt = YouTube(url)
                stream = yt.streams.get_highest_resolution()
                stream.download(DOWNLOAD_FOLDER)
                filename = stream.default_filename
                message = f"YouTube video downloaded: {filename}"
            else:
                filename = url.split("/")[-1]
                response = requests.get(url)
                with open(os.path.join(DOWNLOAD_FOLDER, filename), 'wb') as f:
                    f.write(response.content)
                message = f"File downloaded: {filename}"
        except Exception as e:
            message = f"Error: {str(e)}"
    return render_template('index.html', message=message, filename=filename)

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

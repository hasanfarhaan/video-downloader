from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        format_code = request.form.get('format_code')

        if not url or not format_code:
            return render_template('index.html', error="Please enter a URL and select a format.")

        filename = f"{uuid.uuid4().hex}.%(ext)s"
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        ydl_opts = {
            'outtmpl': filepath,
            'format': format_code,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url)
                final_path = ydl.prepare_filename(info)
            return send_file(final_path, as_attachment=True)
        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

#!/usr/bin/env python3
"""
Saghaugen Filserver - Toveis filutveksling mellom General AI og Ronny.

Funksjoner:
- Last opp filer fra Windows/browser
- Last ned filer som General AI har lagt klar
- Enkel filhåndtering via web-GUI
"""

import http.server
import os
import html
import re
import mimetypes
import urllib.parse
from datetime import datetime
from pathlib import Path

# Konfigurasjon - Auto-detect OS
import platform
if platform.system() == "Windows":
    BASE_DIR = Path("C:/ClaudeCodeProjects/GeneralAI/fildeling")
else:
    BASE_DIR = Path("/home/ronny/ClaudeCodeProjects/GeneralAI/fildeling")
UPLOAD_DIR = BASE_DIR / "fra_ronny"
DOWNLOAD_DIR = BASE_DIR / "til_ronny"
PORT = 8888

# Opprett mapper hvis de ikke finnes
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

def format_size(size_bytes):
    """Formater filstørrelse til lesbar tekst."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def get_file_info(filepath):
    """Hent filinformasjon."""
    stat = filepath.stat()
    return {
        'name': filepath.name,
        'size': format_size(stat.st_size),
        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
    }

HTML_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
    <title>Saghaugen Filserver</title>
    <meta charset="utf-8">
    <style>
        * {{ box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #1a1a2e; color: #eee; }}
        h1 {{ color: #4ecca3; margin-bottom: 5px; }}
        .subtitle {{ color: #888; margin-bottom: 30px; }}
        .section {{ background: #16213e; padding: 25px; border-radius: 10px; margin-bottom: 20px; }}
        h2 {{ color: #4ecca3; margin-top: 0; border-bottom: 1px solid #4ecca3; padding-bottom: 10px; }}
        input[type="file"] {{ margin: 15px 0; }}
        input[type="submit"], .btn {{ background: #4ecca3; color: #1a1a2e; padding: 10px 25px; border: none; border-radius: 5px; cursor: pointer; font-size: 14px; font-weight: bold; text-decoration: none; display: inline-block; }}
        input[type="submit"]:hover, .btn:hover {{ background: #3db892; }}
        .btn-danger {{ background: #e74c3c; color: white; padding: 5px 10px; font-size: 12px; }}
        .btn-danger:hover {{ background: #c0392b; }}
        .success {{ color: #4ecca3; font-weight: bold; padding: 10px; background: rgba(78, 204, 163, 0.1); border-radius: 5px; margin: 10px 0; }}
        .file-list {{ list-style: none; padding: 0; margin: 0; }}
        .file-list li {{ padding: 12px; background: #0f3460; margin: 8px 0; border-radius: 5px; display: flex; justify-content: space-between; align-items: center; }}
        .file-list li:hover {{ background: #1a4a7a; }}
        .file-info {{ display: flex; gap: 20px; align-items: center; }}
        .file-name {{ font-weight: bold; }}
        .file-meta {{ color: #888; font-size: 12px; }}
        .file-actions {{ display: flex; gap: 10px; }}
        .empty {{ color: #666; font-style: italic; padding: 20px; text-align: center; }}
        .two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        @media (max-width: 700px) {{ .two-col {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <h1>Saghaugen Filserver</h1>
    <p class="subtitle">Toveis filutveksling mellom General AI og Ronny</p>

    {message}

    <div class="section">
        <h2>Last opp til General AI</h2>
        <form enctype="multipart/form-data" method="post" action="/upload">
            <input type="file" name="file" multiple required>
            <br>
            <input type="submit" value="Last opp">
        </form>
    </div>

    <div class="two-col">
        <div class="section">
            <h2>Fra Ronny (opplastet)</h2>
            {uploaded_files}
        </div>

        <div class="section">
            <h2>Til Ronny (nedlasting)</h2>
            {download_files}
        </div>
    </div>
</body>
</html>
'''

class FileServerHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")

    def get_file_list_html(self, directory, downloadable=False):
        files = sorted(directory.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)
        files = [f for f in files if f.is_file()]

        if not files:
            return '<p class="empty">Ingen filer</p>'

        items = []
        for f in files:
            info = get_file_info(f)
            encoded_name = urllib.parse.quote(f.name)

            if downloadable:
                actions = f'''
                    <a href="/download/{encoded_name}" class="btn">Last ned</a>
                    <a href="/delete/download/{encoded_name}" class="btn btn-danger" onclick="return confirm('Slette {html.escape(f.name)}?')">Slett</a>
                '''
            else:
                actions = f'''
                    <a href="/view/{encoded_name}" class="btn">Vis</a>
                    <a href="/delete/upload/{encoded_name}" class="btn btn-danger" onclick="return confirm('Slette {html.escape(f.name)}?')">Slett</a>
                '''

            items.append(f'''
                <li>
                    <div class="file-info">
                        <span class="file-name">{html.escape(info['name'])}</span>
                        <span class="file-meta">{info['size']} - {info['modified']}</span>
                    </div>
                    <div class="file-actions">{actions}</div>
                </li>
            ''')

        return f'<ul class="file-list">{"".join(items)}</ul>'

    def send_html(self, message=''):
        uploaded = self.get_file_list_html(UPLOAD_DIR, downloadable=False)
        downloads = self.get_file_list_html(DOWNLOAD_DIR, downloadable=True)

        content = HTML_TEMPLATE.format(
            message=message,
            uploaded_files=uploaded,
            download_files=downloads
        )
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    def send_file(self, filepath):
        if not filepath.exists():
            self.send_error(404, 'File not found')
            return

        mime_type, _ = mimetypes.guess_type(str(filepath))
        if mime_type is None:
            mime_type = 'application/octet-stream'

        self.send_response(200)
        self.send_header('Content-type', mime_type)
        self.send_header('Content-Length', filepath.stat().st_size)

        # For nedlasting, legg til Content-Disposition
        if '/download/' in self.path:
            self.send_header('Content-Disposition', f'attachment; filename="{filepath.name}"')

        self.end_headers()

        with open(filepath, 'rb') as f:
            self.wfile.write(f.read())

    def do_GET(self):
        path = urllib.parse.unquote(self.path)

        if path == '/' or path == '':
            self.send_html()

        elif path.startswith('/download/'):
            filename = path[10:]
            self.send_file(DOWNLOAD_DIR / filename)

        elif path.startswith('/view/'):
            filename = path[6:]
            self.send_file(UPLOAD_DIR / filename)

        elif path.startswith('/delete/upload/'):
            filename = path[15:]
            filepath = UPLOAD_DIR / filename
            if filepath.exists():
                filepath.unlink()
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
            else:
                self.send_error(404)

        elif path.startswith('/delete/download/'):
            filename = path[17:]
            filepath = DOWNLOAD_DIR / filename
            if filepath.exists():
                filepath.unlink()
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
            else:
                self.send_error(404)

        else:
            self.send_error(404)

    def do_POST(self):
        if self.path != '/upload':
            self.send_error(404)
            return

        content_type = self.headers.get('Content-Type', '')
        if 'multipart/form-data' not in content_type:
            self.send_error(400, 'Bad request')
            return

        match = re.search(r'boundary=([^\s;]+)', content_type)
        if not match:
            self.send_error(400, 'No boundary')
            return
        boundary = match.group(1).encode()

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        parts = body.split(b'--' + boundary)
        uploaded_files = []

        for part in parts:
            if b'filename="' not in part:
                continue

            header_end = part.find(b'\r\n\r\n')
            if header_end == -1:
                continue

            header = part[:header_end].decode('utf-8', errors='ignore')
            file_data = part[header_end + 4:]

            if file_data.endswith(b'--\r\n'):
                file_data = file_data[:-4]
            elif file_data.endswith(b'\r\n'):
                file_data = file_data[:-2]

            fn_match = re.search(r'filename="([^"]+)"', header)
            if fn_match and fn_match.group(1):
                filename = fn_match.group(1)
                filepath = UPLOAD_DIR / os.path.basename(filename)
                with open(filepath, 'wb') as f:
                    f.write(file_data)
                uploaded_files.append(filename)

        if uploaded_files:
            file_list = ', '.join(uploaded_files)
            message = f'<div class="success">Lastet opp: {html.escape(file_list)}</div>'
        else:
            message = ''

        self.send_html(message)

if __name__ == '__main__':
    print(f"Saghaugen Filserver starter...")
    print(f"  Upload-mappe:   {UPLOAD_DIR}")
    print(f"  Download-mappe: {DOWNLOAD_DIR}")
    print(f"  URL: http://0.0.0.0:{PORT}")
    print()

    server = http.server.HTTPServer(('0.0.0.0', PORT), FileServerHandler)
    server.serve_forever()

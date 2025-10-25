#!/usr/bin/env python3
"""
====================================================
 A Single-File HTTP Server with Upload Capability
 Modernized for Python 3.13+ (no deprecated `cgi`).
====================================================

 Features:
 - Directory listing + drag-and-drop uploads
 - Multi-file upload support (FormData / XHR)
 - Safe filename sanitization
 - Dedicated "uploads" folder
 - Adjustable upload limit via -s flag (e.g. 4gb, 500mb)
 - Unlimited mode with -s 0
 - Threaded server for parallel uploads
 - Shows local + LAN access URLs
 - Shows QR code via PIL on server startup
"""

import http.server
import socketserver
import os
import argparse
import time
import uuid
import socket
from urllib.parse import unquote
from email.parser import BytesParser
from email.policy import default

# Optional: only import if needed for QR
try:
    import qrcode
except ImportError:
    qrcode = None

# Default settings
UPLOAD_DIR = "uploads"
DEFAULT_MAX_UPLOAD_SIZE = 2 * 1024**3  # 2 GB


# ---------- Helper functions ----------

def get_local_ips():
    """Get 127.0.0.1 and LAN IP (if available)"""
    ips = ['127.0.0.1']
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            lan_ip = s.getsockname()[0]
            if lan_ip != '127.0.0.1':
                ips.append(lan_ip)
    except Exception:
        pass
    # Deduplicate
    seen = set()
    result = []
    for ip in ips:
        if ip not in seen:
            seen.add(ip)
            result.append(ip)
    return result


def show_qr_code(url):
    """Display QR code in a local window using PIL (via qrcode)"""
    if not qrcode:
        print("⚠️  'qrcode' module not installed — skipping QR display.")
        print("   Install with: pip install qrcode[pil]")
        return

    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.show(title="Scan to Open Server")
        print(f"✅ QR code displayed for: {url}")
    except Exception as e:
        print(f"⚠️  Failed to show QR code: {e}")


def sanitize_filename(name: str) -> str:
    """Strip dangerous path characters, nulls, spaces, etc."""
    name = name.replace('\x00', '')
    name = os.path.basename(name.strip())
    if not name:
        name = f"upload_{int(time.time())}"
    return name


def parse_size(size_str: str) -> int:
    """Parse human-readable sizes like 500M, 2G, 4gb, 1024k into bytes."""
    size_str = size_str.strip().lower()
    units = {
        "k": 1024, "kb": 1024,
        "m": 1024**2, "mb": 1024**2,
        "g": 1024**3, "gb": 1024**3,
        "t": 1024**4, "tb": 1024**4
    }
    for suffix, factor in units.items():
        if size_str.endswith(suffix):
            num = float(size_str[:-len(suffix)])
            return int(num * factor)
    return int(size_str)  # assume plain bytes if no suffix


# ---------- Request handler ----------

class UploadHandler(http.server.SimpleHTTPRequestHandler):
    def list_directory(self, path):
        """Generate HTML directory listing + upload UI"""
        try:
            file_list = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None

        file_list.sort(key=lambda a: a.lower())
        displaypath = unquote(self.path)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Upload Server</title>
<style>
body {{
  font-family: Arial, sans-serif; background:#fafafa; margin:0; color:#333;
}}
.container {{
  display:flex; flex-direction:row; height:100vh;
}}
.left,.right {{
  flex:1; padding:20px; overflow-y:auto;
}}
.left {{ border-right:2px solid #eee; }}
ul {{ list-style:none; padding:0; }}
a {{ color:#0066cc; text-decoration:none; }}
a:hover {{ text-decoration:underline; }}
.upload-box {{
  border:2px dashed #bbb; border-radius:10px; padding:20px;
  text-align:center; background:#fff;
}}
.upload-box.dragover {{ background:#e6f7ff; border-color:#3399ff; }}
.progress-container {{ display:none; margin-top:15px; }}
progress {{ width:100%; height:20px; }}
@media(max-width:768px){{
  .container{{flex-direction:column; height:auto;}}
  .left{{border-right:none; border-bottom:2px solid #eee;}}
}}
</style>
</head>
<body>
<div class="container">
  <div class="left">
    <h2>Directory listing for {displaypath}</h2>
    <ul>
"""
        for name in file_list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            html += f'<li><a href="{linkname}">{displayname}</a></li>\n'

        html += """</ul>
  </div>
  <div class="right">
    <h2>Upload Files</h2>
    <div class="upload-box" id="dropZone">
      <p>Drag & drop files here, or click to select</p>
      <form id="uploadForm" method="post" enctype="multipart/form-data">
        <input type="file" id="fileInput" name="file" multiple style="display:none">
        <input type="submit" value="Upload" style="display:none">
      </form>
      <div class="progress-container">
        <progress id="progressBar" value="0" max="100"></progress>
        <p id="status"></p>
      </div>
    </div>
  </div>
</div>
<script>
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const progressBar = document.getElementById('progressBar');
const status = document.getElementById('status');
const progressContainer = document.querySelector('.progress-container');

dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('dragover', e => {{e.preventDefault(); dropZone.classList.add('dragover');}});
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', e => {{
  e.preventDefault();
  dropZone.classList.remove('dragover');
  uploadFiles(e.dataTransfer.files);
}});
fileInput.addEventListener('change', () => uploadFiles(fileInput.files));

function uploadFiles(files) {{
  if (!files.length) return;
  const formData = new FormData();
  for (let f of files) formData.append('file', f);
  const xhr = new XMLHttpRequest();
  progressContainer.style.display = 'block';
  progressBar.value = 0;
  status.textContent = "Uploading...";
  xhr.upload.onprogress = e => {{
    if (e.lengthComputable) {{
      const p = (e.loaded / e.total) * 100;
      progressBar.value = p;
      status.textContent = Math.round(p) + "% uploaded";
    }}
  }};
  xhr.onload = () => {{
    if (xhr.status == 200) {{
      status.textContent = "Upload complete!";
      setTimeout(() => window.location.reload(), 800);
    }} else {{
      status.textContent = "Error: " + xhr.status;
    }}
  }};
  xhr.open("POST", window.location.href);
  xhr.send(formData);
}}
</script>
</body>
</html>"""
        encoded = html.encode("utf-8", "surrogateescape")
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)
        return None

    def do_POST(self):
        """Handle multipart/form-data upload safely (no cgi)"""
        content_type = self.headers.get("Content-Type", "")
        if not content_type.startswith("multipart/form-data"):
            self.send_error(400, "Expected multipart/form-data")
            return

        length = int(self.headers.get("Content-Length", 0))
        if MAX_UPLOAD_SIZE and length > MAX_UPLOAD_SIZE:
            self.send_error(413, f"File too large (>{MAX_UPLOAD_SIZE:,} bytes)")
            return

        body = self.rfile.read(length)
        header_bytes = f"Content-Type: {content_type}\r\n\r\n".encode()
        msg = BytesParser(policy=default).parsebytes(header_bytes + body)

        os.makedirs(UPLOAD_DIR, exist_ok=True)
        saved = []

        for part in msg.iter_parts():
            if part.get_content_disposition() != "form-data":
                continue

            filename = part.get_filename()
            if not filename:
                continue

            filename = sanitize_filename(filename)
            payload = part.get_payload(decode=True)

            base, ext = os.path.splitext(filename)
            dest = os.path.join(UPLOAD_DIR, filename)
            if os.path.exists(dest):
                dest = os.path.join(UPLOAD_DIR, f"{base}_{uuid.uuid4().hex}{ext}")

            with open(dest, "wb") as f:
                f.write(payload)
            saved.append(os.path.basename(dest))

        if saved:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"Uploaded: {', '.join(saved)}".encode())
        else:
            self.send_error(400, "No files uploaded")


# ---------- Server runner ----------

def run_server(directory, port):
    os.chdir(directory)
    ips = get_local_ips()
    urls = [f"http://{ip}:{port}" for ip in ips]

    # Choose best URL for QR: prefer non-localhost
    qr_url = urls[0]
    for url in urls:
        if not url.startswith("http://127.0.0.1"):
            qr_url = url
            break

    # Show QR code in a local window (if qrcode is available)
    show_qr_code(qr_url)

    # Print info
    host_ip = socket.gethostbyname(socket.gethostname())
    limit_str = f"{MAX_UPLOAD_SIZE / (1024**3):.1f} GB" if MAX_UPLOAD_SIZE else "unlimited"
    print(f"\n🌐 Serving HTTP on all interfaces (0.0.0.0:{port})")
    print(f"Local access   → http://127.0.0.1:{port}")
    print(f"Network access → http://{host_ip}:{port}")
    print(f"Serving directory: {os.path.abspath(directory)}")
    print(f"Uploads saved in: {os.path.abspath(UPLOAD_DIR)}")
    print(f"Upload size limit: {limit_str}\n")

    with socketserver.ThreadingTCPServer(("", port), UploadHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")


# ---------- Main entry ----------
    handler = UploadHandler

    with socketserver.ThreadingTCPServer(("", port), handler) as httpd:
        host_ip = socket.gethostbyname(socket.gethostname())
        limit_str = f"{MAX_UPLOAD_SIZE / (1024**3):.1f} GB" if MAX_UPLOAD_SIZE else "unlimited"
        print(f"\n🌐 Serving HTTP on all interfaces (0.0.0.0:{port})")
        print(f"Local access   → http://127.0.0.1:{port}")
        print(f"Network access → http://{host_ip}:{port}")
        print(f"Serving directory: {os.path.abspath(directory)}")
        print(f"Uploads saved in: {os.path.abspath(UPLOAD_DIR)}")
        print(f"Upload size limit: {limit_str}\n")
        httpd.serve_forever()


# ---------- Main entry ----------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simple HTTP Upload Server (modern, configurable)"
    )
    parser.add_argument(
        "-d", "--directory", default=".",
        help="Directory to serve files from (default: current dir)"
    )
    parser.add_argument(
        "-p", "--port", type=int, default=8000,
        help="Port to serve on (default: 8000)"
    )
    parser.add_argument(
        "-s", "--size-limit", default="2gb",
        help="Max upload size (e.g. 500mb, 4gb, 0=unlimited)"
    )

    args = parser.parse_args()
    MAX_UPLOAD_SIZE = parse_size(args.size_limit) if args.size_limit != "0" else 0

    run_server(args.directory, args.port)

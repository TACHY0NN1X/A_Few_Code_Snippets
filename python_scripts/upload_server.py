#!/usr/bin/env python3

#################################################
# A Single File Http Server with Upload Feature #
#################################################


import http.server
import socketserver
import os
import argparse
import cgi
from urllib.parse import unquote

class UploadHandler(http.server.SimpleHTTPRequestHandler):
    def list_directory(self, path):
        """Custom directory listing + upload form"""
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
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        background: #fafafa;
        color: #333;
    }}
    .container {{
        display: flex;
        flex-direction: row;
        height: 100vh;
        box-sizing: border-box;
    }}
    .left, .right {{
        flex: 1;
        padding: 20px;
        overflow-y: auto;
        min-width: 0;
    }}
    .left {{
        border-right: 2px solid #eee;
    }}
    h2 {{
        margin-top: 0;
    }}
    ul {{
        list-style: none;
        padding: 0;
    }}
    li {{
        margin: 5px 0;
        word-break: break-all;
    }}
    a {{
        text-decoration: none;
        color: #0066cc;
    }}
    a:hover {{
        text-decoration: underline;
    }}
    .upload-box {{
        border: 2px dashed #bbb;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background: #fff;
        transition: background 0.3s;
    }}
    .upload-box.dragover {{
        background: #e6f7ff;
        border-color: #3399ff;
    }}
    .progress-container {{
        margin-top: 15px;
        display: none;
    }}
    progress {{
        width: 100%;
        height: 20px;
    }}
    @media (max-width: 768px) {{
        .container {{
            flex-direction: column;
            height: auto;
        }}
        .left {{
            border-right: none;
            border-bottom: 2px solid #eee;
        }}
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
const form = document.getElementById('uploadForm');
const progressBar = document.getElementById('progressBar');
const status = document.getElementById('status');
const progressContainer = document.querySelector('.progress-container');

// click on dropZone to trigger file input
dropZone.addEventListener('click', () => fileInput.click());

// drag & drop visual feedback
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    fileInput.files = e.dataTransfer.files;
    uploadFiles(fileInput.files);
});

// handle manual file selection
fileInput.addEventListener('change', () => {
    uploadFiles(fileInput.files);
});

function uploadFiles(files) {
    if (!files.length) return;
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {{
        formData.append('file', files[i]);
    }}

    const xhr = new XMLHttpRequest();
    progressContainer.style.display = 'block';
    progressBar.value = 0;
    status.textContent = "Uploading...";

    xhr.upload.onprogress = function(e) {
        if (e.lengthComputable) {
            let percent = (e.loaded / e.total) * 100;
            progressBar.value = percent;
            status.textContent = Math.round(percent) + "% uploaded";
        }
    };

    xhr.onload = function() {
        if (xhr.status == 200) {
            status.textContent = "Upload complete!";
            setTimeout(() => window.location.reload(), 1000);
        } else {
            status.textContent = "Error: " + xhr.status;
        }
    };

    xhr.open("POST", window.location.href);
    xhr.send(formData);
}
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
        """Handle file uploads with multipart parser (preserves filename)"""
        content_type = self.headers.get('content-type')
        if not content_type:
            self.send_error(400, "Bad Request: Missing Content-Type header")
            return

        ctype, pdict = cgi.parse_header(content_type)
        if ctype == 'multipart/form-data':
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            pdict['CONTENT-LENGTH'] = int(self.headers['content-length'])
            form = cgi.FieldStorage(fp=self.rfile,
                                    headers=self.headers,
                                    environ={'REQUEST_METHOD':'POST',
                                             'CONTENT_TYPE':content_type})
            if "file" in form:
                fields = form["file"]
                if not isinstance(fields, list):
                    fields = [fields]

                for field in fields:
                    if field.filename:
                        filename = os.path.basename(field.filename)
                        with open(os.path.join(os.getcwd(), filename), "wb") as f:
                            f.write(field.file.read())
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"File(s) uploaded successfully")
        else:
            self.send_error(400, "Bad Request: Expected multipart/form-data")


def run_server(directory, port):
    os.chdir(directory)
    handler = UploadHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving HTTP on port {port}, directory: {directory}")
        httpd.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple HTTP Upload Server")
    parser.add_argument("-d", "--directory", default=".", help="Directory to serve files from")
    parser.add_argument("-p", "--port", type=int, default=8000, help="Port to serve on")
    args = parser.parse_args()

    run_server(args.directory, args.port)


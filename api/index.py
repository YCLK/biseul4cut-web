from flask import Flask, request, send_from_directory, render_template_string
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# 업로드된 파일을 저장할 폴더
UPLOAD_FOLDER = './upload'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    # 파일 업로드 처리
    f = request.files['file']
    filename = secure_filename(f.filename)
    f.save(os.path.join(UPLOAD_FOLDER, filename))
    return f"File {filename} uploaded successfully!"

@app.route('/<filename>', methods=['GET'])
def preview_and_download(filename):
    # 파일 경로 확인
    file_path = os.path.join(UPLOAD_FOLDER, f"{filename}.png")
    if not os.path.exists(file_path):
        return "File not found.", 404
    
    # HTML 페이지 템플릿
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @font-face {
                font-family: 'Pretendard-Regular';
                src: url('https://fastly.jsdelivr.net/gh/Project-Noonnu/noonfonts_2107@1.1/Pretendard-Regular.woff') format('woff');
                font-weight: 400;
                font-style: normal;
            }
        </style>
        <script>
            tailwind.config = {
                theme: {
                    extend: {
                        fontFamily: {
                            sans: ["Pretendard-Regular", "sans-serif"], 
                        },
                    }
                }
            }
        </script>
        <title>비슬네컷</title>
    </head>
    <body class="bg-gray-100 flex flex-col items-center justify-center min-h-screen p-6">
        <h1 class="text-4xl font-bold mb-6 font-sans">비슬네컷</h1>
        <img src="/uploads/{{ filename }}.png" class="w-1/4 mb-6 border border-gray-300 shadow-lg"/>
        <a href="/download/{{ filename }}">
            <button class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700 font-sans">다운로드</button>
        </a>
        <footer class="mt-10 text-gray-500 font-sans">2024 엔지니어스</footer>

    </body>
    </html>
    """
    return render_template_string(html_template, filename=filename)

@app.route('/uploads/<path:filename>')
def serve_file(filename):
    # upload 폴더에서 파일을 제공
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # 파일 다운로드 처리
    file_path = os.path.join(UPLOAD_FOLDER, f"{filename}.png")
    if os.path.exists(file_path):
        return send_from_directory(UPLOAD_FOLDER, f"{filename}.png", as_attachment=True)
    else:
        return "File not found.", 404

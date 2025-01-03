import os
import subprocess

# 설정
VIDEOS_DIR = "/var/www/html/videos"  # 동영상 파일 폴더 경로
THUMBNAILS_DIR = "/var/www/html/thumbnails"  # 썸네일 저장 경로
INDEX_FILE = "/var/www/html/index.html"  # 생성할 index.html 경로
TITLE_IMAGE = "math_thumbnail.webp"

# HTML 템플릿
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:image" content="{title_image}">
    <title>Video Gallery</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            color: #333;
            margin: 0;
            padding: 20px;
        }}
        h1 {{
            text-align: center;
        }}
        ul {{
            list-style-type: none;
            padding: 0;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
        }}
        li {{
            margin: 10px;
            padding: 10px;
            background: #fff;
            border: 1px solid #ddd;
            border-radius: 5px;
            text-align: center;
            flex: 1 1 calc(25% - 20px);  /* 기본 크기: 3개씩 */
            box-sizing: border-box;
        }}
        img {{
            max-width: 100%;
            height: auto;
            object-fit: cover;
            border-radius: 5px;
        }}
        a {{
            text-decoration: none;
            color: #007bff;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .video-title {{
            font-size: 14px;
            line-height: 1.2;
            max-height: 2.4em;
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
        }}
        @media (max-width: 768px) {{
            li {{
                flex: 1 1 calc(33.3333% - 20px);
            }}
        }}
        @media (max-width: 480px) {{
            li {{
                flex: 1 1 calc(50% - 20px);
            }}
        }}
    </style>
</head>
<body>
    <h1>Video Gallery</h1>
    <ul>
        {file_links}
    </ul>
</body>
</html>
"""

def get_video_duration(video_path):
    """
    동영상의 총 길이(초 단위)를 반환합니다.
    """
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return float(result.stdout.strip()) if result.returncode == 0 else 0

def seconds_to_hhmmss(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{secs:02}"

def print_progress(current, total, task_name):
    """
    간단한 진행률 출력.
    """
    percent = (current / total) * 100
    print(f"\r{task_name}: {current}/{total} ({percent:.1f}%)", end="", flush=True)

def generate_video_thumbnails(videos_dir, thumbnails_dir):
    # 썸네일 디렉토리가 없으면 생성
    os.makedirs(thumbnails_dir, exist_ok=True)

    video_files = [f for f in os.listdir(videos_dir) if f.endswith((".mp4", ".avi", ".mov"))]
    total_files = len(video_files)

    for i, file_name in enumerate(video_files, start=1):
        if file_name.endswith((".mp4", ".avi", ".mov")):  # 동영상 파일만 처리
            video_path = os.path.join(videos_dir, file_name)
            thumbnail_name = f"{os.path.splitext(file_name)[0]}.jpg"
            thumbnail_path = os.path.join(thumbnails_dir, thumbnail_name)

            # 동영상 길이 계산
            duration = get_video_duration(video_path)
            thumbnail_time = seconds_to_hhmmss(duration / 3)

            # ffmpeg를 사용해 썸네일 생성
            subprocess.run([
                "ffmpeg", "-y", "-ss", thumbnail_time, "-i", video_path,  "-vframes", "1", thumbnail_path
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
            # 진행률 출력
            print_progress(i, total_files, "Generating Thumbnails")
        

def generate_index_html(videos_dir, thumbnails_dir, index_file, title_image):
    # HTML 파일 생성
    file_links = ""
    for file_name in os.listdir(videos_dir):
        if file_name.endswith((".mp4", ".avi", ".mov")):  # 동영상 파일만 처리
            thumbnail_name = f"{os.path.splitext(file_name)[0]}.jpg"
            file_links += f"""
            <li>
                <a href="videos/{file_name}">
                    <img src="thumbnails/{thumbnail_name}" alt="{file_name} thumbnail">
                    <div class="video-title">{file_name}</div>
                </a>
            </li>
            """

    # HTML 파일 쓰기
    with open(index_file, "w") as f:
        html_content = HTML_TEMPLATE.format(file_links=file_links, title_image=title_image)
        f.write(html_content)

# 실행
generate_video_thumbnails(VIDEOS_DIR, THUMBNAILS_DIR)
generate_index_html(VIDEOS_DIR, THUMBNAILS_DIR, INDEX_FILE, TITLE_IMAGE)

# 최종 출력
print(f"index.html created at {INDEX_FILE}")

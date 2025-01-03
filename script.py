import os

# HTML 파일 경로
directory = "/var/www/html"
html_file = os.path.join(directory, "index.html")

# 디렉토리 내 파일 목록 가져오기
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# HTML 파일 생성
with open(html_file, "w") as f:
    f.write("<!DOCTYPE html>\n<html>\n<head>\n<title>My Files</title>\n</head>\n<body>\n")
    f.write("<h1>Available Files</h1>\n<ul>\n")
    for file in files:
        f.write(f'<li><a href="{file}">{file}</a></li>\n')
    f.write("</ul>\n</body>\n</html>\n")

print(f"Custom index.html generated at {html_file}")

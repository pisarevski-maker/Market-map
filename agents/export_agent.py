#!/usr/bin/env python3
"""
Export Agent - Czech Steel Dashboard
Generates Docker packaging files and copies dashboard to output/.

Usage:
    python agents/export_agent.py
"""

import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR   = PROJECT_ROOT / "output" / "czech-steel-dashboard"

DOCKERFILE = """\
FROM nginx:alpine
COPY dashboard/ /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""

NGINX_CONF = """\
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;

    gzip on;
    gzip_types text/html text/css application/javascript application/json image/svg+xml;

    location ~* \\.html$ {
        add_header Cache-Control "no-cache";
    }

    location ~* \\.(js|css|svg|png|ico|json)$ {
        add_header Cache-Control "public, max-age=31536000";
    }

    location / {
        try_files $uri $uri/ =404;
    }
}
"""

COMPOSE = """\
version: "3.8"
services:
  dashboard:
    build: .
    container_name: czech-steel-dashboard
    ports:
      - "8080:80"
    restart: unless-stopped
"""

RUN_BAT = "@echo off\ndocker compose up --build -d\necho Dashboard at http://localhost:8080\nstart http://localhost:8080\n"
RUN_SH  = "#!/bin/bash\ndocker compose up --build -d\necho 'Dashboard at http://localhost:8080'\n"


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  wrote: {path.relative_to(PROJECT_ROOT)}")


def main():
    print("Export Agent - Czech Steel Dashboard")
    print("=====================================")

    write(OUTPUT_DIR / "Dockerfile",         DOCKERFILE)
    write(OUTPUT_DIR / "nginx.conf",         NGINX_CONF)
    write(OUTPUT_DIR / "docker-compose.yml", COMPOSE)
    write(OUTPUT_DIR / "run.bat",            RUN_BAT)
    write(OUTPUT_DIR / "run.sh",             RUN_SH)

    src = PROJECT_ROOT / "dashboard"
    dst = OUTPUT_DIR / "dashboard"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print(f"  copied: dashboard/ -> output/czech-steel-dashboard/dashboard/")

    print("\nDone. To launch:")
    print("  Windows: double-click output/czech-steel-dashboard/run.bat")
    print("  Linux:   bash output/czech-steel-dashboard/run.sh")


if __name__ == "__main__":
    main()

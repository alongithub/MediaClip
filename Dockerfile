FROM python:3.8-slim

ENV TZ="Asia/Shanghai"
ENV TimeZone="Asia/Shanghai"
ENV LANG=C.UTF-8

COPY docker/sources.list /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
    imagemagick \
    ffmpeg

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/


CMD ["python", "main.py"]
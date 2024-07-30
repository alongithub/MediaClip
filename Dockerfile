FROM python:3.8-slim

ENV TZ="Asia/Shanghai"
ENV TimeZone="Asia/Shanghai"
ENV LANG=C.UTF-8

COPY docker/sources.list /etc/apt/sources.list
COPY docker/resolv.conf /etc/resolv.conf

RUN apt-get update && apt-get install -y \
    imagemagick

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com




CMD ["python", "main.py"]
# MediaClip

音视频处理用到的一些工具api

## features
- [x] 音频生成字幕，
- [x] 字幕校对
- [x] srt 2 video
- [ ] 语言检测
- [ ] fast-wisper
- [ ] funasr
- [ ] 音频分割
- [ ] webui

## init

### 安装 imagemagick
```bash
# for mac
brew install imagemagick

# for linux
sudo apt-get update
sudo apt-get install imagemagick
```

### 安装 python 环境
```bash
conda create -n media-clip python=3.8
conda activate media-clip
pip install -r requirements.txt
```

## usage

### run
1. by conda
```bash
python main.py
```

2. by docker
```bash
docker build -t media-clip:v0.1 .
docker compose -f docker-compose.yml up -d
```

### api doc

localhost:3335/docs

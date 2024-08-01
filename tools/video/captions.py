from moviepy.editor import TextClip, VideoFileClip, CompositeVideoClip
from pysrt import open as open_srt
from infra.logger import logger
from typing import List

def get_area_size(video_size: List[int], area_size: List[int]):
    width = area_size[0]
    height = area_size[1]
    
    if width == 0:
        width = video_size[0]
    elif width > 0 and width <= 1:
        width = int(video_size[0] * width)
    elif width > 1:
        width = width
    else:
        width = video_size[0]
        
    if height == 0:
        height = None
    elif height > 0 and height <= 1:
        height = int(video_size[1] * height)
    elif height > 1:
        height = height
    else:
        height = None

    return (width, height)

def get_area_position(area_position: List[str]):
    x = area_position[0]
    y = area_position[1]

    return (x, y)

def font_list():
    return TextClip.list('font')

def color_list():
    return TextClip.list('color')
   

def srt_caption(
    srt_file: str, 
    video_file: str,
    output_path: str,
    
    stroke_color: str,
    stroke_width: int,
    bg_color: str,
    fontsize: int = 60,
    font_color: str = 'white',
    kerning: int = 0,
    area_size: List[int] = [0.8, 0],
    area_position: List[str] = ['center', 'bottom'],
       
):
    logger.debug(f"srt：{srt_file} \nvideo: {video_file}")
    subs = open_srt(srt_file)
    video_clip = VideoFileClip(video_file)
    
    subclips = []
    
    size = get_area_size(video_clip.size, area_size)
    position = get_area_position(area_position)

    # 为每个字幕创建一个TextClip，并将其添加到subclips列表中
    for sub in subs:
        text = sub.text
        start = sub.start.ordinal / 1000.0  # 将字幕开始时间转换为秒
        end = sub.end.ordinal / 1000.0  # 将字幕结束时间转换为秒
        # logger.debug("add_caption: %s",text)
        subclip = TextClip(
            text, 
            fontsize=fontsize, 
            color=font_color, 
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            bg_color=bg_color, 
            method='caption', # caption label 
            align="center", 
            kerning=kerning,
            size=size,
            font="/Library/Fonts/Arial Unicode.ttf", 
            # font="兰亭黑-简-中黑",
        )
        subclip = subclip.set_start(start).set_end(end).set_position(position)
        subclips.append(subclip)
        
    final_clip = CompositeVideoClip([video_clip] + subclips)
    
    final_clip.write_videofile(
        output_path, 
        codec='libx264', 
        audio_codec='aac', 
        fps=video_clip.fps,
        # threads=8,
        # preset='medium',
        # bitrate='5000k'
    )
    
    return output_path
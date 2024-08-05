from typing import List
import whisper



def execute_asr(
    audio_path: str,
    model_size: str = "small", # "tiny", "base", "small", "medium", "large-v2"
    language: str = "zh", 
):
    model = whisper.load_model(model_size)
    result = model.transcribe(
        audio_path,
        initial_prompt="输出中文简体",
    )
    return result["segments"]


# 保留静音片段，默认从两端中间切割，最长500ms
def keep_slice(segments: List[dict], keep_silent: int = 0):
    last_end = 0
    next_start = 0
    for index, segment in enumerate(segments):  
        if index != 0:
            last_end = segments[index - 1]['end']
        if index != len(segments) - 1:
            next_start = segments[index + 1]['start']
        else:
            next_start = segment['end']
            
        start, end = segment['start'], segment['end']
        if start - last_end >= keep_silent * 2:
            segment['start'] = start - keep_silent
        else:
            segment['start'] = start - (start - last_end) / 2
            
        if next_start - end >= keep_silent * 2:
            segment['end'] = end + keep_silent
        else:
            segment['end'] = end + (next_start - end) / 2
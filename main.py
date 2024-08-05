import os
from fastapi import FastAPI, Body, HTTPException
from middleware.logger import LoggerMiddleware
from pydantic import BaseModel, Field
from tools.asr.whisper_asr import execute_asr, keep_slice
from tools.audio.slice import AudioSlicer
from tools.srt import check_diff
from tools.srt import Srt, save_srts
from tools.video.captions import srt_caption
import uvicorn
from typing import List

app = FastAPI()
app.add_middleware(LoggerMiddleware)

class AddSrtRequest(BaseModel):
    srt_file: str
    video_file: str
    output_path: str
    fontsize: int = 60
    font_color: str = '#fff'
    stroke_color: str = 'rgba(0, 0, 0, 0)'
    stroke_width: int = 0
    bg_color: str = 'rgba(0, 0, 0, 0)'
    kerning: int = 0
    area_size: List[int] = [0.8, 0]
    area_position: List[str] = ["center", "bottom"]

class AddSrtRequests(BaseModel):
    output_path: str


@app.post("/video/add_srt_to_video", response_model=AddSrtRequests)
async def add_srt_to_video(
    body: AddSrtRequest = Body(...),
):
    srt_caption(
        body.srt_file, video_file=body.video_file, output_path=body.output_path,
        fontsize=body.fontsize, font_color=body.font_color, stroke_color=body.stroke_color,
        stroke_width=body.stroke_width, bg_color=body.bg_color, kerning=body.kerning,
        area_size=body.area_size, area_position=body.area_position
    )
    
    return AddSrtRequests(output_path=body.output_path)

class Audio2StrRequest(BaseModel):
    ref_text: str = Field("", description="原始文案，通过提供原始文案可以使asr结果更准确。请确保文案与音频内容一致")
    audio_file: str = Field(description="音频文件")
    output_path: str = Field(description="输出路径，确保路径存在")
    
class Audio2StrResponse(BaseModel):
    output_path: str
    
@app.post("/audio/gen_audio_srt", response_model=Audio2StrResponse)
async def gen_audio_srt(
    body: Audio2StrRequest = Body(...),
):
    segments = execute_asr(body.audio_file)
    srts = [Srt(s["id"], s["text"], s["start"], s["end"]) for s in segments]
    
    if body.ref_text != "":
        check_diff.check_srt_diff(srts, body.ref_text)

    save_srts(srts, body.output_path)
    return Audio2StrResponse(output_path=body.output_path)

class AudioSliceRequest(BaseModel):
    audio_file: str = Field(description="音频文件夹或音频文件")
    output_dir: str = Field(description="输出文件夹，确保路径存在")
    min_length: float = Field(description="最小切片时长，单位为秒")
    max_length: float = Field(description="最大切片时长，单位为秒")
    keep_silent: float = Field(0.0, description="保留片段前后静音的时长，单位为秒")
    sliding_slice: bool = Field(False, description="是否使用滑动窗口切片")
    
class AudioSliceResponse(BaseModel):
    output_audios: List[str]

def get_slice_list(segments: List[dict], max_length: int = 12, min_length: int = 8, sliding_slice: bool = False):
    slice_list = []
    temp_list = []
    for i, s in enumerate(segments):
        temp_list.append(s)
        while len(temp_list) > 0:
            total_duration = sum(t['end'] - t['start'] for t in temp_list)
            if total_duration > max_length:
                temp_list.pop(0)
            elif total_duration < min_length:
                break
            else:
                slice_list.append({
                    "start": temp_list[0]['start'],
                    "end": temp_list[-1]['end'],
                })
                if sliding_slice:
                    # 如果提供音频太短，使用滑动窗口重复利用片段
                    temp_list.pop(0); 
                    continue 
                else:
                    # 所有片段只使用一次
                    temp_list.clear()
    
    return slice_list          

@app.post("/audio/slice_audio", response_model=AudioSliceResponse)
async def slice_audio(
    body: AudioSliceRequest = Body(...),
):
    if os.path.isdir(body.audio_file):
        audio_files = [os.path.join(body.audio_file, f) for f in os.listdir(body.audio_file) if f.endswith('.wav')]
    elif os.path.isfile(body.audio_file) and body.audio_file.endswith('.wav'):
        audio_files = [body.audio_file]
    else:
        raise HTTPException(
            status_code=400, 
            detail="请提供有效的音频文件夹或音频文件,音频文件必须是wav格式",
        )
        
    output_audios = []
    
    for audio_file in audio_files:
        base_name = os.path.basename(audio_file)
        segments = execute_asr(audio_file)
        keep_slice(segments, body.keep_silent) # 保持最长0.5s的静默时间
        slice_list = get_slice_list(segments, sliding_slice=body.sliding_slice, max_length=body.max_length, min_length=body.min_length)         

        audio =  AudioSlicer(audio_file)
        for s in slice_list:
            start = s['start']
            end = s['end']
            output_audio = os.path.join(body.output_dir, f'{base_name}_{start}_{end}.wav')
            audio.slice(start, end, output_audio)
            output_audios.append(output_audio)
            
    return AudioSliceResponse(output_audios=output_audios)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3336)
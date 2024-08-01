from fastapi import FastAPI, Body
from middleware.logger import LoggerMiddleware
from pydantic import BaseModel, Field
from tools.asr.whisper_asr import execute_asr
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


@app.post("/video/add_srt_to_video")
async def add_srt_to_video(
    body: AddSrtRequest = Body(...),
):
    return srt_caption(
        body.srt_file, video_file=body.video_file, output_path=body.output_path,
        fontsize=body.fontsize, font_color=body.font_color, stroke_color=body.stroke_color,
        stroke_width=body.stroke_width, bg_color=body.bg_color, kerning=body.kerning,
        area_size=body.area_size, area_position=body.area_position
    )
    
class Audio2StrRequest(BaseModel):
    ref_text: str = Field("", description="原始文案，通过提供原始文案可以使asr结果更准确。请确保文案与音频内容一致")
    audio_file: str = Field(description="音频文件")
    output_path: str = Field(description="输出路径，确保路径存在")
    
@app.post("/audio/gen_audio_srt")
async def gen_audio_srt(
    body: Audio2StrRequest = Body(...),
):
    segments = execute_asr(body.audio_file)
    srts = [Srt(s["id"], s["text"], s["start"], s["end"]) for s in segments]
    
    if body.ref_text != "":
        check_diff.check_srt_diff(srts, body.ref_text)

    save_srts(srts, body.output_path)
    return body.output_path

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3336)
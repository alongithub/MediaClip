from fastapi import FastAPI, Body
from pydantic import BaseModel
from utils.text.captions import font_list, srt_caption
import uvicorn


# print(font_list())

app = FastAPI()

class SrtRequest(BaseModel):
    srt_file: str
    video_file: str
    output_path: str
    fontsize: int = 60
    font_color: str = '#fff'
    stroke_color: str = 'rgba(0, 0, 0, 0)'
    stroke_width: int = 0
    bg_color: str = 'rgba(0, 0, 0, 0)'
    kerning: int = 0
    area_size: list[int] = [0.8, 0]
    area_position: list[str] = ["center", "bottom"]


@app.post("/caption/srt")
async def srt(
    body: SrtRequest = Body(...),
):
    return srt_caption(
        body.srt_file, video_file=body.video_file, output_path=body.output_path,
        fontsize=body.fontsize, font_color=body.font_color, stroke_color=body.stroke_color,
        stroke_width=body.stroke_width, bg_color=body.bg_color, kerning=body.kerning,
        area_size=body.area_size, area_position=body.area_position
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3340)
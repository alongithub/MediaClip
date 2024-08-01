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
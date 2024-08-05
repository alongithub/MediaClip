import soundfile as sf

class AudioSlicer():
    def __init__(self, audio_file_path: str ):
        self.audio_file_path = audio_file_path
        self.load_audio()
        
    def load_audio(self):
        audio, sr = sf.read(self.audio_file_path)
        self.audio_length = len(audio) / sr
        self.audio = audio
        self.sr = sr

    def slice(self,  start: float, end: float, output_audio_file_path: str):
        start_frame =start * self.sr
        end_frame = end * self.sr
        audio_segment = self.audio[int(start_frame):int(end_frame)]  # 使用numpy数组切片来获取音频片段
        sf.write(output_audio_file_path, audio_segment, self.sr)  # 保存音频片段  
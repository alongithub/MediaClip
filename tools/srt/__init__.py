from typing import List


class Srt():
    text: str
    start: str
    end: str
    id: int
    
    def __init__(self, id: int, text: str, start: str, end: str):
        self.id = id
        self.text = text
        self.start = start
        self.end = end
        

    def format(self):
        text = self.text.strip()
        srt = f"{self.id + 1}\n{self.convert_time_format(self.start)} --> {self.convert_time_format(self.end)}\n{text}"
        return srt
    
    def conver_time_by_seconds(self, seconds):
        hours = str(int(seconds // 3600))
        minutes = str(int((seconds % 3600) // 60))
        seconds = seconds % 60
        milliseconds = str(int(int((seconds - int(seconds)) * 1000))) # 毫秒留三位
        seconds = str(int(seconds))
        # 补0
        if len(hours) < 2:
            hours = '0' + hours
        if len(minutes) < 2:
            minutes = '0' + minutes
        if len(seconds) < 2:
            seconds = '0' + seconds
        if len(milliseconds) < 3:
            milliseconds = '0'*(3-len(milliseconds)) + milliseconds
        return f"{hours}:{minutes}:{seconds},{milliseconds}"
    
    def convert_time_format(self, seconds: float):
        # 格式为 秒
        return self.conver_time_by_seconds(seconds)

def save_srts(srts: List[Srt], output_path: str):
    
    with open(output_path, "w", encoding="utf-8") as srt_file:
        srt_file.write(
            "\n\n".join(
                [srt.format() for srt in srts]
            )
        )
        
   
    
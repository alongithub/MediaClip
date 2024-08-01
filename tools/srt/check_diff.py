# 提取text中的token,keep_space会将标点转换为空格
import difflib
from typing import List

from tools.srt import Srt

def tokens_in_text(text, keep_space=False):
    # 中文
    def is_chinese(char):
        return '\u4e00' <= char <= '\u9fff'

    # 日文
    def is_japanese(char):
        return ('\u3040' <= char <= '\u309F') or ('\u30A0' <= char <= '\u30FF') or ('\u4E00' <= char <= '\u9FBF')

    # 数字
    def is_digit(char):
        return char.isdigit()

    words = []
    current_word = []
    space = False

    for char in text:
        if is_chinese(char) or is_japanese(char) or is_digit(char):
            if space:
                space = False
                words.append(" ")
            
            if current_word:
                words.append(''.join(current_word))
                current_word = []
            words.append(char)
        elif char.isalpha():
            current_word.append(char)
        else:
            if current_word:
                if space:
                    space = False
                    words.append(" ")
                
                words.append(''.join(current_word))
                current_word = []
                
                
            if keep_space:
                space = True

    if current_word:
        words.append(''.join(current_word))

    return words, len([item for item in words if item != " "])

# 从tokens中获取length个有效token
def get_tokens(tokens, length):
    ts = []
    ci = 0
    while length > 0 and ci < len(tokens):
        t = tokens[ci]
        ci += 1
        ts.append(t)
        if t != " ":
            length -= 1
            
    return ts




# 将diff 排序，如果 +- 是连续的，将相应数量的-提取到+之前
def sort_diffs(diffs: List[str]):
    add_num = 0
    add_index = []
    
    for index, d in enumerate(diffs):
        if d.startswith(" "):
            add_num = 0
        elif d.startswith("+"):
            add_num += 1
            add_index.append(index)
            
        elif d.startswith("-"):
            if add_num > 0 and d != "-  ":
                ai = add_index.pop(0)
                diffs[index] = diffs[ai]
                diffs[ai] = d
                add_num -= 1
    
    
# 修正srtlist 中的文案 srtlist 格式为 list[dict], dict 需要包含 text字段
# prompt_text 为参考文案
def check_srt_diff(srtlist: List[Srt], prompt_text):
    tokens, _ = tokens_in_text(prompt_text, True)
    for index,srt in enumerate(srtlist):
        if index == len(srtlist) - 1:
            srt.text = "".join(tokens)
            break
        
        srt_tokens, srt_length = tokens_in_text(srt.text)
        
        diff = list(difflib.ndiff(
            get_tokens(tokens, srt_length + 3),
            srt_tokens
        ))
        sort_diffs(diff)
        
        new_text = ""
        
        for d in diff:
            if len(srt_tokens) == 0:
                break
            if d.startswith("-"):
                new_text += tokens.pop(0)
            elif d.startswith("+"):
                srt_tokens.pop(0)
                pass
            elif d.startswith(" "):
                new_text += tokens.pop(0)
                srt_tokens.pop(0)
            
        srt.text = new_text
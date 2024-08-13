import os
import traceback

from funasr import AutoModel

path_asr  = 'tools/asr/models/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch'
path_vad  = 'tools/asr/models/speech_fsmn_vad_zh-cn-16k-common-pytorch'
path_punc = 'tools/asr/models/punc_ct-transformer_zh-cn-common-vocab272727-pytorch'
path_asr  = path_asr  if os.path.exists(path_asr)  else "iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
path_vad  = path_vad  if os.path.exists(path_vad)  else "iic/speech_fsmn_vad_zh-cn-16k-common-pytorch"
path_punc = path_punc if os.path.exists(path_punc) else "iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch"

model = AutoModel(
    model               = path_asr,
    model_revision      = "v2.0.4",
    vad_model           = path_vad,
    vad_model_revision  = "v2.0.4",
    punc_model          = path_punc,
    punc_model_revision = "v2.0.4",
)

def only_asr(input_file):
    try:
        text = model.generate(input=input_file)[0]["text"]
    except:
        text = ''
        print(traceback.format_exc())
    return text
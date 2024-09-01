from torch import Tensor
from torchaudio import info
import torchaudio.functional as F

def stereo_to_mono(audio: Tensor) -> Tensor:
    if audio.shape[0] == 2:
        return audio.mean(0)
    return audio

def downsample(
    audio: Tensor, 
    current_rate: int,
    new_rate: int,
) -> Tensor:
    if current_rate != new_rate:
        return F.resample(audio, current_rate, new_rate)
    return audio

def get_duration(filename: str) -> float:
    md = info(filename)
    return md.num_frames / md.sample_rate

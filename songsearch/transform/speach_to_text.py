from typing import Optional, Tuple
from torch import Tensor
from torch.cuda import is_available as cuda_is_available
from faster_whisper import WhisperModel, BatchedInferencePipeline

STT_SAMPLE_RATE = 16000

def transcribe(audio: Tensor, language: Optional[str] = None) -> Tuple[str, str]:
    
    model_size = "large-v3"
    device = "cuda" if cuda_is_available() else "cpu"

    model = WhisperModel(model_size, device=device)

    assert model.feature_extractor.sampling_rate == STT_SAMPLE_RATE

    batched_model = BatchedInferencePipeline(model=model)
    try:
        segments, info = batched_model.transcribe(
            audio, 
            batch_size=16, 
            language=language,
        )
    except RuntimeError as e:
        if str(e) == "stack expects a non-empty TensorList":
            # No active speech found in audio
            return ('','')
        else:
            raise(e)

    return (
        ' '.join([seg.text for seg in segments]), 
        info.language
    )

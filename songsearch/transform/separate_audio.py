from typing import Tuple
from pathlib import Path

from demucs.api import Separator
from torch import Tensor

SEPARATOR_MODELS_PATH = "./models"
SEPARATOR_MODEL_REMOTE_PATH = "hybrid_transformer/04573f0d-f3cf25b2.th"
SEPARATOR_MODEL_NAME = "htdemucs_ft_vocals"

def extract_vocals(
    file_path: str,
    model_name: str,
    model_path: str,
    source_name: str = 'vocals',
) -> Tuple[Tensor, int]:

    separator = Separator(model=model_name,
                          repo=Path(model_path),
                          # device=args.device,
                          # shifts=args.shifts,
                          split=True,
                          overlap=0.1,
                          progress=True,
                          # jobs=2,
                          # segment=1 #args.segment
                          )


    origin, separated = separator.separate_audio_file(file_path)

    return separated[source_name], separator.samplerate

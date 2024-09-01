from typing import Optional
from songsearch.repository.tracks import insert_one, record_exists, search_similar
from songsearch.transform.grapheme_to_phoneme import convert_g2p

MAX_DURATION = 6*60

def index(glob_pattern: str, language: Optional[str] = None) -> None:

    from demucs.pretrained import ROOT_URL as MODEL_REMOTE_URL
    import torch as th
    import glob
    import tqdm
    
    from songsearch.transform.separate_audio import SEPARATOR_MODELS_PATH, SEPARATOR_MODEL_REMOTE_PATH, SEPARATOR_MODEL_NAME, SEPARATOR_MODEL_NAME, extract_vocals
    from songsearch.transform.speach_to_text import STT_SAMPLE_RATE, transcribe
    from songsearch.transform.utils import stereo_to_mono, downsample, get_duration
    from songsearch.utils import download_file, get_hashsum


    for filename in tqdm.tqdm(glob.glob(glob_pattern)):
        file_hashsum = get_hashsum(filename)
    
        duration = get_duration(filename=filename)
    
        if not record_exists(file_hashsum) and duration < MAX_DURATION:
    
            print(f'Processing {filename}...')
    
            download_file(url=MODEL_REMOTE_URL + SEPARATOR_MODEL_REMOTE_PATH,
                          folder=SEPARATOR_MODELS_PATH)
    
            vocals, sample_rate = extract_vocals(file_path=filename, model_name=SEPARATOR_MODEL_NAME, model_path=SEPARATOR_MODELS_PATH)
    
            vocals = stereo_to_mono(vocals)
            vocals = downsample(vocals, sample_rate, STT_SAMPLE_RATE)
    
            lyrics, language = transcribe(vocals, language)
    
            print(lyrics)
    
            phonemics = convert_g2p(lyrics)
    
            insert_one(
                hashsum = file_hashsum,
                title = filename,
                lyrics = lyrics,
                phonemics = phonemics,
                language = language,
            )
    
        else:
            print(f'Skipping {filename}...')
    
def search(query: str) -> None:
    for rec in search_similar(
            lyrics = query,
            phonemics = convert_g2p(query)
    ):
        print(rec)

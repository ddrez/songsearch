import os
import urllib.request
import hashlib
from pathlib import Path

def download_file(
    url: str,
    folder: str,
) -> None:
    filename = Path(folder) / url.split('/')[-1]
    if not os.path.exists(filename):
        print(f'Downloading {url} into {folder}...')
        urllib.request.urlretrieve(url, filename)

def get_hashsum(filename: str) -> str:
    st = os.stat(filename)
    return hashlib.md5('{filename}~{size}'.format(filename=filename, size=st.st_size).encode('utf-8')).hexdigest()

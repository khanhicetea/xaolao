import requests
from tempfile import NamedTemporaryFile
from pydub import AudioSegment

def convert_audio(in_file : NamedTemporaryFile, from_format, to_format) -> NamedTemporaryFile:
    sound = AudioSegment.from_file(in_file.name, from_format)
    out_file = NamedTemporaryFile('w+b')
    sound.export(out_file.name, format=to_format)
    in_file.close()
    return out_file

def download_file(url : str) -> NamedTemporaryFile:
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        in_file = NamedTemporaryFile('w+b')
        for chunk in r.iter_content(chunk_size=8192): 
            in_file.write(chunk)
    return in_file

def convert_url(url, from_fomat, to_format):
    in_file = download_file(url)
    out_file = convert_audio(in_file, from_fomat, to_format)
    return out_file

def close_file_after_res(f):
    f.close()

from pydub import AudioSegment 
from typing import Union
from pydub import AudioSegment
from utils import *

def split_audio(
    input_file:Union[str,Path],
    ts_file:list[dict],
    output_folder:Union[str,Path] = None
):
    input_file = str2path(input_file)
    ts_file = str2path(ts_file)
    output_folder = str2path(output_folder) if output_folder else input_file.parent/input_file.stem
    
    if not output_folder.exists():
        output_folder.mkdir()

    
    ts_d = loadtsfile(ts_file)
    
    audio = AudioSegment.from_file(input_file)
    for i,limit in enumerate(ts_d):
        if limit['start'] == '0':
            limit['start'] = '0:0:0'
        clip = audio[time2msec(limit['start']):time2msec(limit['end'])]
        clip.export(output_folder/f"{limit['speaker']}_{i}.mp3", format='mp3')

def merge_mp3s(
    parent_path:Union[str, Path],
    maxlength:int = 9
):
    p = str2path(parent_path)
    silence = AudioSegment.silent(duration=1500)
    for path in p.ls():
        if path.is_dir():
            combined = AudioSegment.empty()            
            count = 0
            MP3_FILES = path.rglob('**/*.mp3')
            MP3_FILES = list(MP3_FILES)
            for i, mp3 in enumerate(MP3_FILES):
                try:
                    combined += AudioSegment.from_file(mp3.as_posix())
                    combined += silence
                except:
                    continue
                count += 1
                if count >= maxlength:
                    combined.export(path/f"{path.stem}_{i}.mp3", format='mp3')
                    combined = AudioSegment.empty()   
                    count = 0
                    print(f"batch {i} {path} Merged")
                elif i+1 == len(MP3_FILES):
                    combined.export(path/f"{path.stem}_{i}.mp3", format='mp3')
            _ = [x.unlink() for x in MP3_FILES]
            print(f"Directory {path} Merged")
            

    
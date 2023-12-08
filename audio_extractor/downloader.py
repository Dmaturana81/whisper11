
from pytube import YouTube
from pytube.innertube import InnerTube
import pytube.exceptions as exceptions
from typing import Union
import os
from fastcore.all import *
from utils import *

@patch
def bypass_age_gate2(self: YouTube):
        """Attempt to update the vid_info by bypassing the age gate."""
        innertube = InnerTube(
            client='ANDROID',
            use_oauth=self.use_oauth,
            allow_cache=self.allow_oauth_cache
        )
        innertube_response = innertube.player(self.video_id)

        playability_status = innertube_response['playabilityStatus'].get('status', None)

        # If we still can't access the video, raise an exception
        # (tier 3 age restriction)
        if playability_status == 'UNPLAYABLE':
            raise exceptions.AgeRestrictedError(self.video_id)

        self._vid_info = innertube_response

def load_video(url, **kwargs):
    """Function to load youtube video"""
    return YouTube(url, use_oauth=True, allow_oauth_cache=True)

def download_youtube_audio(url, out_dir=".", out_fname=None, best_quality=True):
    "Download the audio from a YouTube video"
    yt = load_video(url)
    if out_fname is None:
        out_fname = os.path.join(out_dir, to_snake_case(yt.title) + ".mp4")
    else:
        out_fname = os.path.join(out_dir,out_fname)
    try:
        yt.streams
    except exceptions.AgeRestrictedError as e:
        print(f"ERROR: {e}")
        yt.bypass_age_gate2()
    yt = (yt.streams
        .filter(only_audio=True, file_extension="mp4")
        .order_by("abr"))
    if best_quality:
        yt = yt.desc()
    else:
        yt = yt.asc()
    return yt.first().download(filename=out_fname)

def download_all(file:Union[str,Path]):
    file = file if isinstance(file,Path) else Path(file)
    with open(file,'r') as infile:
        urls = infile.readlines()
    if len(urls) == 0:
        print(f"{file} has no urls")
    for i, url in enumerate(urls):
        if file.parent.joinpath(file.stem).joinpath(f"{file.stem}_{i}.mp3").exists():
            print(f"""{file.parent.joinpath(file.stem).joinpath(f"{file.stem}_{0}.mp3")} Exists""")
            continue
        download_youtube_audio(url, out_dir=f"{file.parent}/{file.stem}/", out_fname=f"{file.stem}_{i}.mp3")

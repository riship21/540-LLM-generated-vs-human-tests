import re

KNOWN_EXTENSIONS = {'mp4', 'webm', 'mkv', 'flv', 'mov'}

def determine_ext(url, default_ext='unknown_video'):
    if url is None:
        return default_ext
    guess = url.partition('?')[0].rpartition('.')[2]
    if re.match(r'^[A-Za-z0-9]+$', guess):
        return guess
    elif guess.rstrip('/') in KNOWN_EXTENSIONS:
        return guess.rstrip('/')
    else:
        return default_ext

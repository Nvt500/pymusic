import os
import sys

def get_songs_dir() -> str:
    home = os.path.dirname(sys.argv[0])
    return os.path.join(home, "songs")

def get_playlists_dir() -> str:
    home = os.path.dirname(sys.argv[0])
    return os.path.join(home, "playlists")

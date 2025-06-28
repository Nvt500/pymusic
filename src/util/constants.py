import os
import sys
from enum import Enum

import click


def get_songs_dir() -> str:
    return os.path.join(get_executable_path(), "songs")

def get_playlists_dir() -> str:
    return os.path.join(get_executable_path(), "playlists")

def get_cookies_path() -> str:
    return os.path.join(get_executable_path(), "cookies.txt")

def get_executable_path() -> str:
    return os.path.dirname(sys.argv[0])


class GetSongPathError(Enum):
    NO_SONGS_DIR = 0,
    NO_SONG_FILE = 1,

def get_song_path(name: str) -> str | GetSongPathError:

    # Get path to songs folder
    songs_path = get_songs_dir()
    if not os.path.exists(songs_path):
        click.echo(f"Songs directory doesn't exist at {songs_path}.")
        return GetSongPathError.NO_SONGS_DIR

    # Add .mp3 if not specified
    if not name.endswith(".mp3"):
        name += ".mp3"

    # Get path to song
    song_path = os.path.join(songs_path, name)
    if not os.path.exists(song_path):
        click.echo(f"The song {song_path} doesn't exist.\n")
        return GetSongPathError.NO_SONG_FILE

    return song_path
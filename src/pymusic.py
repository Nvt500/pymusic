import os
import click

from src.play.play import play
from src.download.download import download
from src.song import song
from src.playlist import playlist
from src.util.constants import get_songs_dir, get_playlists_dir


@click.group()
@click.help_option('-h', '--help')
def cli() -> None:
    """A cli to download and play music."""
    pass

@cli.command()
@click.help_option('-h', '--help')
def init() -> None:
    """Creates "songs" and "playlists" folder

    If you don't feel like doing it for some reason.
    """

    songs_path = get_songs_dir()
    playlists_path = get_playlists_dir()
    os.makedirs(songs_path, exist_ok=True)
    os.makedirs(playlists_path, exist_ok=True)

cli.add_command(play)
cli.add_command(download)
cli.add_command(song)
cli.add_command(playlist)
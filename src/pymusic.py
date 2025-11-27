import os
import click

from src.play.play import play
from src.download.download import download
from src.song import song
from src.playlist import playlist
from src.util.constants import get_songs_dir, get_playlists_dir, get_cookies_path


@click.group()
@click.help_option("-h", "--help")
@click.version_option("0.2.3", "-v", "--version", message="%(prog)s %(version)s", prog_name="pymusic")
def cli() -> None:
    """A cli to download and play music."""
    pass

@cli.command()
@click.help_option("-h", "--help")
def init() -> None:
    """Creates "songs" and "playlists" folder and "cookies.txt" """

    songs_path = get_songs_dir()
    playlists_path = get_playlists_dir()
    cookies_path = get_cookies_path()

    os.makedirs(songs_path, exist_ok=True)
    os.makedirs(playlists_path, exist_ok=True)
    if not os.path.exists(cookies_path):
        with open(cookies_path, "x") as cookies_file:
            cookies_file.close()

    click.echo(f"Created:\n{songs_path}\n{playlists_path}\n{cookies_path}")


cli.add_command(play)
cli.add_command(download)
cli.add_command(song)
cli.add_command(playlist)


if __name__ == "__main__":
    cli()
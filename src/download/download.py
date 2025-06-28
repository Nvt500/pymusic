import os
import click
import yt_dlp
from typing import Callable
from moviepy.audio.io.AudioFileClip import AudioFileClip

from src.util.constants import get_songs_dir, get_playlists_dir, get_cookies_path


@click.command()
@click.help_option('-h', '--help')
@click.argument("url")
@click.option("-r", "--replace", "replace", default=False, is_flag=True, help="Replace file if it already exists.")
@click.option("-t", "--to-playlist", "to_playlist", default=None, type=str, help="Name of playlist to download to.", metavar="NAME")
@click.option("-n", "--no-cookies", "no_cookies", default=False, is_flag=True, help="Do not download using cookies.")
def download(url: str, replace: bool, to_playlist: str, no_cookies: bool) -> None:
    """Download music from url

    URL is a url to a YouTube video or PUBLIC playlist.
    (wrap url in quotes if there is an & in the url at least on windows cmd)
    """
    if not no_cookies and not os.path.exists(get_cookies_path()):
        click.echo("cookies.txt does not exist.")
        return
    elif not no_cookies and os.path.exists(get_cookies_path()):
        with open(get_cookies_path(), "r") as f:
            if f.read().strip() == "":
                click.echo("cookies.txt is empty.")
                return

    try:
        songs, playlist_name = download_url(url, replace, no_cookies)

        if "playlist" in url:
            add_songs_to_playlist(songs, playlist_name if to_playlist is None else to_playlist)
        else:
            if to_playlist is not None:
                add_songs_to_playlist(songs, to_playlist)
    except click.Abort:
        pass
    except Exception as e:
        click.echo(f"Error occurred: {e}.")


# Do this to use replace, pretty cool ngl
def init_download_hook(replace: bool, songs: list[str]) -> Callable[[dict], None]:

    def download_hook(status_dict: dict) -> None:
        if status_dict["status"] == "downloading":
            click.echo(f"Downloading {status_dict['info_dict']['title']}...\r", nl=False)
        elif status_dict["status"] == "error":
            click.echo(f"Error occurred: {status_dict['info_dict']['message']}.\r")
        elif status_dict["status"] == "finished":
            click.echo(f"Downloaded {status_dict['info_dict']['title']}.\r", nl=False)

            title = os.path.basename(status_dict["info_dict"]["filename"])
            title = title.rsplit(".", 1)[0]
            new_title = "".join([c for c in title if c.isalnum()]) + ".mp4"
            os.rename(os.path.join(get_songs_dir(), title + ".mp4"), os.path.join(get_songs_dir(), new_title))

            path = os.path.join(get_songs_dir(), new_title)
            new_path = path.rsplit(".", 1)[0] + ".mp3"
            if replace or (not replace and not os.path.exists(new_path)):
                if os.path.exists(new_path):
                    os.remove(new_path)
                audio = AudioFileClip(path)
                audio.write_audiofile(new_path, logger=None)
                click.echo(f"Finished at {new_path}.\r")
            else:
                click.echo(f"{new_path} already exists.\r")
            os.remove(path)

            songs.append(new_title[:-1] + "3")

    return download_hook


def download_url(url: str, replace: bool, no_cookies: bool) -> (list[str], str | None):

    songs = []

    options = {
        "progress_hooks": [init_download_hook(replace, songs)],
        "quiet": True,
        "outtmpl": os.path.join(get_songs_dir(), "%(title)s.%(ext)s"),
        "no_warnings": True,
        "noprogress": True,
        "restrictfilenames": True,
        "ignoreerrors": True,
    }
    if not no_cookies:
        options["cookiefile"] = get_cookies_path()

    with yt_dlp.YoutubeDL(options) as ydl:
        info_dict: dict = ydl.extract_info(url, download=True)
        if "entries" in info_dict.keys():
            return songs, info_dict["title"]
        else:
            return songs, None


def add_songs_to_playlist(songs: list[str], to_playlist: str) -> None:

    # Get playlist path
    playlists_path = get_playlists_dir()

    playlists = os.listdir(playlists_path)

    if to_playlist not in playlists and click.confirm(f"{to_playlist} does not exist, do you want to create it?", abort=True):
        os.makedirs(os.path.join(playlists_path, to_playlist))

    if not os.path.exists(os.path.join(playlists_path, to_playlist, "songs.txt")):
        with open(os.path.join(playlists_path, to_playlist, "songs.txt"), "w") as file:
            file.close()

    # Append to songs.txt
    with open(os.path.join(playlists_path, to_playlist, "songs.txt"), "r+") as file:
        lines = [line.strip() for line in file.readlines() if line.strip() != ""]
        lines.extend(songs)

        lines = set(lines)

        file.seek(0)
        file.truncate()
        file.write("\n".join(lines))
        file.close()

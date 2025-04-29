import concurrent.futures
import os
import click
from moviepy.audio.io.AudioFileClip import AudioFileClip
from pytubefix import YouTube, Playlist

from src.util.constants import get_songs_dir, get_playlists_dir


@click.command()
@click.help_option('-h', '--help')
@click.argument("url")
@click.option("-w", "--with-out-oauth", "oauth", default=False, is_flag=True, help="Download without oauth.")
@click.option("-r", "--replace", "replace", default=False, is_flag=True, help="Replace file if it already exists.")
@click.option("-t", "--to-playlist", "to_playlist", default=None, type=str, help="Name of playlist to download to.", metavar="NAME")
@click.option("-s", "--sync", "sync", default=False, is_flag=True, help="Turn off asynchronous downloading.")
@click.option("-m", "--max-workers", "max_workers", default=5, show_default=True, type=int, help="Input into ThreadPoolExecutor when async.")
def download(url: str, oauth: bool, replace: bool, to_playlist: str, sync: bool, max_workers: int) -> None:
    """Download music from url

    URL is a url to a YouTube video or PUBLIC playlist.
    (wrap url in quotes if there is an & in the url at least on windows cmd)
    """
    try:
        if "playlist" in url:
            songs, to_playlist = download_playlist(url, oauth, replace, sync, max_workers)
        else:
            song_name = download_song(url, oauth, replace)
            songs = [song_name]

        if to_playlist is not None:
            add_songs_to_playlist(songs, to_playlist)
    except click.Abort:
        pass
    except Exception as e:
        click.echo(f"Error occurred: {e}.")


def download_playlist(url, oauth: bool, replace: bool, sync: bool, max_workers: int) -> (list[str], str):

    playlist = Playlist(url, use_oauth=oauth, allow_oauth_cache=oauth)

    title = playlist.title

    click.echo(f"Downloading playlist {title}.")

    if sync:
        songs = []
        for video in playlist.video_urls:
            click.echo(f"Downloading {len(songs) + 1}/{len(playlist.video_urls)}")
            songs.append(download_song(video, oauth, replace))

        return songs, title

    with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
        # Get video urls in list because enumerating directly gives waring in pycharm
        video_urls = [video_url for video_url in playlist.video_urls]
        # Make dictionary to sort later to keep order
        futures = {i: executor.submit(download_song, video_url, oauth, replace) for i, video_url in enumerate(video_urls)}
        # Get dictionary of results
        results = {i: future.result()  for i, future in futures.items()}

    # Since results are tagged by 0-(len-1) do a for loop to get everything in correct order
    res = []
    for i in range(len(results.keys())):
        res.append(results.get(i))
    results = res

    return results, title

def download_song(url: str, oauth: bool, replace: bool) -> str:

    # Get YouTube object
    youtube = YouTube(url, use_oauth=oauth, allow_oauth_cache=oauth)#, use_po_token=True)
    songs_path = get_songs_dir()

    if not os.path.exists(songs_path) and click.confirm(f"{songs_path} does not exist, do you want to create it?", abort=True):
        os.makedirs(songs_path)

    # Use this to make sure there isn't anything wierd to mess stuff up.
    title = "".join([c for c in youtube.title if c.isalnum()]) + ".mp4"
    file_path = os.path.join(songs_path, title)

    # Replace file if it exists
    if os.path.exists(file_path.removesuffix(".mp4") + ".wav"):
        if replace:
            os.remove(file_path)
        else:
            click.echo(f"{file_path.removesuffix(".mp4") + ".wav"} already exists.")
            return os.path.basename(file_path.removesuffix(".mp4") + ".wav")

    # Download file
    click.echo(f"Downloading at {file_path}.")
    stream = youtube.streams.get_lowest_resolution()
    path = stream.download(output_path=songs_path, filename=title)
    click.echo(f"Downloaded at {path}.")

    # Convert mp4 to wav because downloading as mp3 doesn't work with pytube
    new_path = path.rstrip(".mp4") + ".wav"
    audio = AudioFileClip(path)
    audio.write_audiofile(new_path, logger=None)
    os.remove(path)
    click.echo(f"Finished at {new_path}.")

    return os.path.basename(new_path)


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

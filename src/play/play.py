import os
import time
import wave
import click
from pywinctl import getActiveWindowTitle
from random import shuffle
if os.name == "nt":
    import winsound

# Remove message from pygame
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from pygame import mixer

from src.util.key_handler import KeyHandler
from src.util.constants import get_songs_dir, get_playlists_dir, get_song_path, GetSongPathError
from src.util.selector import Selector


@click.group()
@click.help_option('-h', '--help')
def play() -> None:
    """Play music"""


@play.command()
@click.help_option('-h', '--help')
@click.argument("name")
@click.option("-l", "--low-cpu", "low_cpu", default=False, is_flag=True, help="Stripped down music player to hopefully take up less resources")
@click.option("-r", "--repeat", "repeat", default=False, is_flag=True, help="Repeat a song (forever)")
def song(name: str, low_cpu: bool, repeat: bool) -> None:
    """Play song"""

    if low_cpu and os.name != "nt":
        click.echo("Low CPU mode is only for windows.")
        return

    _song(name, low_cpu, repeat)

def _song(name: str, low_cpu: bool, repeat: bool = False) -> None:

    terminal_name = getActiveWindowTitle()

    if not low_cpu:
        mixer.init()

    song_path = get_song_path(name)

    if isinstance(song_path, GetSongPathError):
        return

    click.clear()

    # Play song
    while True:
        try:
            play_song(song_path, low_cpu, terminal_name)
        except KeyboardInterrupt:
            click.echo()
            break
        if not repeat:
            break


@play.command()
@click.help_option('-h', '--help')
@click.argument("name")
@click.option("-r", "--random", "random", default=False, is_flag=True, help="Randomize playlist")
@click.option("-l", "--low-cpu", "low_cpu", default=False, is_flag=True, help="Stripped down music player to hopefully take up less resources")
def playlist(name: str, random: bool, low_cpu: bool) -> None:
    """Play playlist"""

    if low_cpu and os.name != "nt":
        click.echo("Low CPU mode is only for windows.")
        return

    _playlist(name, random, low_cpu)

def _playlist(name: str, random: bool, low_cpu: bool) -> None:

    terminal_name = getActiveWindowTitle()

    if not low_cpu:
        mixer.init()

    # Get path to playlists folder
    playlists_path = get_playlists_dir()
    if not os.path.exists(playlists_path):
        click.echo(f"Playlists directory doesn't exist at {playlists_path}.")
        return

    # Check playlist of name exists
    playlists = os.listdir(playlists_path)
    if name not in playlists:
        click.echo(f"The playlist \"{name}\" does not exist.")
        return

    playlist_path = os.path.join(playlists_path, name)

    if not os.path.exists(os.path.join(playlist_path, "songs.txt")):
        click.echo(f"songs.txt doesn't exist at {os.path.join(playlist_path, 'songs.txt')}.")
        return

    # Get songs
    with open(os.path.join(playlist_path, "songs.txt"), "r") as file:
        songs = [line.strip() for line in file.readlines() if line.strip() != ""]
        file.close()

    # Randomize songs
    if random:
        shuffle(songs)

    click.clear()

    playlist_volume = [10]

    # Play each song
    click.echo(f"Playing playlist {name}.\nCtrl-C to quit.\n")
    try:
        for song_name in songs:
            song_path = get_song_path(song_name)

            if song_path is GetSongPathError.NO_SONG_FILE:
                continue
            elif song_path is GetSongPathError.NO_SONGS_DIR:
                return

            play_song(song_path, low_cpu, terminal_name, playlist_volume)
    except KeyboardInterrupt:
        click.echo()


def play_song(song_path: str, low_cpu, terminal_name: str, volume_pointer: list[int] = None) -> None:

    if low_cpu:
        click.echo(f"Playing {os.path.basename(song_path)}.\n")
        # Need all this or Ctrl-C doesn't work
        wav = wave.open(song_path, "rb")
        duration = wav.getnframes() / wav.getframerate()
        winsound.PlaySound(song_path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT | winsound.SND_NOSTOP | winsound.SND_NOWAIT)
        start = time.time()
        while time.time() - start < duration:
            pass
        return

    click.echo(f"Playing {os.path.basename(song_path)}.\nSpace to (un)pause, enter to skip/stop, arrow keys to control volume.")

    sound = mixer.Sound(song_path)
    sound.play()

    duration = sound.get_length()
    duration_m, duration_s = divmod(int(duration), 60)

    now = time.time()
    then = now
    time_passed = 0.0

    volume: int = volume_pointer[0] if volume_pointer is not None else 10

    sound.set_volume(volume / 10)

    handler = KeyHandler(terminal_name)

    is_paused = False
    while mixer.get_busy() or is_paused:
        match handler.getch():
            case "space":
                if is_paused:
                    mixer.unpause()
                else:
                    mixer.pause()
                is_paused = not is_paused
            case "enter":
                sound.stop()
                is_paused = False
            case "up":
                if volume < 10:
                    volume += 1
                    sound.set_volume(volume / 10)
            case "down":
                if volume > 0:
                    volume -= 1
                    sound.set_volume(volume / 10)

        now = time.time()
        if not is_paused:
            time_passed += now - then
        then = now

        m, s = divmod(int(time_passed), 60)
        click.echo(f"{m:02d}:{s:02d}/{duration_m:02d}:{duration_s:02d} | Volume: {volume:02d}\r", nl=False)

    sound.stop()
    mixer.music.unload()
    handler.close()

    click.echo("\n")

    if volume_pointer is not None:
        volume_pointer[0] = volume


@play.command()
@click.help_option('-h', '--help')
@click.argument("which")
@click.option("--max-items", default=5, type=click.IntRange(1, 9, clamp=True), help="Maximum number of items displayed per page")
@click.option("-r", "--random", "random", default=False, is_flag=True, help="Randomize playlist (only applies when WHICH is \"playlist\")")
@click.option("-l", "--low-cpu", "low_cpu", default=False, is_flag=True, help="Stripped down music player to hopefully take up less resources")
def select(which: str, max_items: int, random: bool, low_cpu: bool) -> None:
    """Select a song or playlist to play.

    \b
    WHICH can be:
        "song" - select a song
        "playlist" - select a playlist
        "from-playlist" - select a playlist then a song from that playlist

    "song" is the default.
    """

    if low_cpu and os.name != "nt":
        click.echo("Low CPU mode is only for windows.")
        return

    get_from = False
    if which.lower() in ["from-playlist", "from_playlist", "fromplaylist"]:
        get_from = True

    if which.lower() == "playlist" or get_from:
        # Get playlists
        playlists_path = get_playlists_dir()
        if not os.path.exists(playlists_path):
            click.echo(f"Playlists directory doesn't exist at {playlists_path}.")
            return

        playlists = os.listdir(playlists_path)

        # Select playlist
        try:
            playlist_name = Selector.select(playlists, max_items)
        except KeyboardInterrupt:
            return

        if not get_from:
            # Do playlist action with selected playlist
            _playlist(playlist_name, random, low_cpu)
            return

        playlist_path = os.path.join(playlists_path, playlist_name)

        if not os.path.exists(os.path.join(playlist_path, "songs.txt")):
            click.echo(f"songs.txt doesn't exist at {os.path.join(playlist_path, 'songs.txt')}.")
            return

        # Get songs
        with open(os.path.join(playlist_path, "songs.txt"), "r") as file:
            songs = [line.strip() for line in file.readlines() if line.strip() != ""]
            file.close()

        try:
            song_name = Selector.select(songs, max_items)
        except KeyboardInterrupt:
            return

        # Do song action with selected song
        _song(song_name, low_cpu)
    else:
        # Get songs
        songs_path = get_songs_dir()
        if not os.path.exists(songs_path):
            click.echo(f"Songs directory doesn't exist at {songs_path}.")
            return

        songs = os.listdir(songs_path)

        # Select song
        try:
            song_name = Selector.select(songs, max_items)
        except KeyboardInterrupt:
            return

        # Do song action with selected song
        _song(song_name, low_cpu)
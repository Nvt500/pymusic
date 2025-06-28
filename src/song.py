import os
import click

from src.util.constants import get_songs_dir, get_song_path, GetSongPathError, get_playlists_dir


@click.group()
@click.help_option('-h', '--help')
def song() -> None:
    """Rename, delete, and list songs"""
    pass


@song.command(short_help="Rename a song")
@click.help_option('-h', '--help')
@click.argument("name")
def rename(name: str) -> None:
    """Rename a song in the "songs" directory and all occurrences in each playlist's songs.txt

    Be aware that os.path.join and os.path.exists doesn't care about capitals so if you are not
    careful the name in "songs" may be different from in the songs.txt.
    """

    song_path = get_song_path(name)
    if isinstance(song_path, GetSongPathError):
        return

    if not name.endswith(".mp3"):
        name += ".mp3"

    new_name = click.prompt(f"What is the new name of {name}", type=click.STRING)

    if not new_name.endswith(".mp3"):
        new_name += ".mp3"

    click.echo(f"Renamed {name} to {new_name} from {song_path}.")
    new_song_path = song_path.replace(name, new_name)
    os.rename(song_path, new_song_path)

    playlists_path = get_playlists_dir()
    if not os.path.exists(playlists_path):
        click.echo(f"Playlists directory doesn't exist at {playlists_path}.")
        return

    for playlist in os.listdir(playlists_path):
        path = os.path.join(playlists_path, playlist, "songs.txt")
        if not os.path.exists(path):
            click.echo(f"{path} does not have a songs.txt.")
            continue

        with open(path, "r+") as file:
            lines = [line.strip() for line in file.readlines() if line.strip() != ""]
            if lines.count(name) > 0:
                click.echo(f"Renamed {name} to {new_name} from {path}.")
            while lines.count(name) > 0:
                lines[lines.index(name)] = new_name

            file.seek(0)
            file.truncate()
            file.write("\n".join(lines))
            file.close()


@song.command(short_help="Delete a song")
@click.help_option('-h', '--help')
@click.argument("name")
def delete(name: str) -> None:
    """Deletes a song in the "songs" directory and all occurrences in each playlist's songs.txt"""

    song_path = get_song_path(name)

    if isinstance(song_path, GetSongPathError):
        return

    if not name.endswith(".mp3"):
        name += ".mp3"

    if not click.confirm(f"Are you sure you want to delete {name}?"):
        click.echo(f"Not deleting {name}.")
        return

    os.remove(song_path)

    click.echo(f"Removed {name} from {song_path}.")

    playlists_path = get_playlists_dir()
    if not os.path.exists(playlists_path):
        click.echo(f"Playlists directory doesn't exist at {playlists_path}.")
        return

    for playlist in os.listdir(playlists_path):
        path = os.path.join(playlists_path, playlist, "songs.txt")
        if not os.path.exists(path):
            click.echo(f"{path} does not have a songs.txt.")
            continue

        with open(path, "r+") as file:
            lines =  [line.strip() for line in file.readlines() if line.strip() != ""]
            if lines.count(name) > 0:
                click.echo(f"Removed {name} from {path}.")
            while lines.count(name) > 0:
                lines.remove(lines[lines.index(name)])

            file.seek(0)
            file.truncate()
            file.write("\n".join(lines))
            file.close()


@song.command(name="list")
@click.help_option('-h', '--help')
def list_songs() -> None:
    """List songs"""

    songs_path = get_songs_dir()
    if not os.path.exists(songs_path):
        click.echo(f"Songs directory doesn't exist at {songs_path}.")
        return

    for i, song_name in enumerate(os.listdir(songs_path)):
        click.echo(f"{i+1}. {song_name.removesuffix('.mp3')}")
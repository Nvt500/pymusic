import os
import shutil
import click

from src.util.constants import get_playlists_dir, get_song_path, GetSongPathError


@click.group()
@click.help_option('-h', '--help')
def playlist() -> None:
    """Rename, delete, list, list songs, add to, remove from, and create playlists"""


@playlist.command()
@click.help_option('-h', '--help')
@click.argument("name")
def rename(name: str) -> None:
    """Rename a playlist"""

    playlists_path = get_playlists_dir()
    if not os.path.exists(playlists_path):
        click.echo(f"Playlists directory doesn't exist at {playlists_path}.")
        return

    playlist_path = os.path.join(playlists_path, name)
    if not os.path.exists(playlist_path):
        click.echo(f"Playlist doesn't exist at {playlist_path}.")
        return

    new_name = click.prompt(f"What is the new name of {name}", type=click.STRING)

    click.echo(f"Renamed {name} to {new_name} from {playlist_path}.")
    new_playlist_path = playlist_path.replace(name, new_name)
    os.rename(playlist_path, new_playlist_path)


@playlist.command()
@click.help_option('-h', '--help')
@click.argument("name")
def delete(name: str) -> None:
    """Delete a playlist"""

    playlists_path = get_playlists_dir()
    if not os.path.exists(playlists_path):
        click.echo(f"Playlists directory doesn't exist at {playlists_path}.")
        return

    playlist_path = os.path.join(playlists_path, name)
    if not os.path.exists(playlist_path):
        click.echo(f"Playlist doesn't exist at {playlist_path}.")
        return

    if not click.confirm(f"Are you sure you want to delete {name}?"):
        click.echo(f"Not deleting {name}.")
        return

    shutil.rmtree(playlist_path)

    click.echo(f"Removed {name} from {playlist_path}.")


@playlist.command(name="list")
@click.help_option('-h', '--help')
def list_playlists() -> None:
    """List playlists"""

    playlists_path = get_playlists_dir()
    if not os.path.exists(playlists_path):
        click.echo(f"Playlists directory doesn't exist at {playlists_path}.")
        return

    for i, playlist_name in enumerate(os.listdir(playlists_path)):
        click.echo(f"{i+1}. {playlist_name}")


@playlist.command(name="songs")
@click.help_option('-h', '--help')
@click.argument("name")
def list_songs(name: str) -> None:
    """List songs from a playlist

    NAME is the name of the playlist to list songs from.
    """

    playlists_path = get_playlists_dir()
    if not os.path.exists(playlists_path):
        click.echo(f"Playlists directory doesn't exist at {playlists_path}.")
        return

    playlist_path = os.path.join(playlists_path, name)
    if not os.path.exists(playlist_path):
        click.echo(f"Playlist doesn't exist at {playlist_path}.")
        return

    with open(os.path.join(playlist_path, "songs.txt"), "r") as file:
        lines = [line.strip() for line in file.readlines() if line.strip() != ""]

        for i, line in enumerate(lines):
            print(f"{i+1}. {line}")

        file.close()


@playlist.command()
@click.help_option('-h', '--help')
@click.argument("name")
def add(name: str) -> None:
    """Add a song to a playlist

    NAME is the name of the song to add.
    """

    song_path = get_song_path(name)
    if isinstance(song_path, GetSongPathError):
        return

    if not name.endswith(".wav"):
        name += ".wav"

    playlists_path = get_playlists_dir()
    if not os.path.exists(playlists_path):
        click.echo(f"Playlists directory doesn't exist at {playlists_path}.")
        return

    playlist_name = click.prompt(f"What playlist to add to", type=click.STRING)

    playlist_path = os.path.join(playlists_path, playlist_name)
    if not os.path.exists(playlist_path):
        click.echo(f"Playlist doesn't exist at {playlist_path}.")
        return

    with open(os.path.join(playlist_path, "songs.txt"), "r+") as file:
        lines = [line.strip() for line in file.readlines() if line.strip() != ""]
        lines.append(name)

        file.seek(0)
        file.truncate()
        file.write("\n".join(lines))
        file.close()

    click.echo(f"Added {name} to {os.path.join(playlist_path, "songs.txt")}.")


@playlist.command()
@click.help_option('-h', '--help')
@click.argument("name")
def remove(name: str) -> None:
    """Remove a song from a playlist

    NAME is the name of the song to remove.
    """

    song_path = get_song_path(name)
    if isinstance(song_path, GetSongPathError):
        return

    if not name.endswith(".wav"):
        name += ".wav"

    playlists_path = get_playlists_dir()
    if not os.path.exists(playlists_path):
        click.echo(f"Playlists directory doesn't exist at {playlists_path}.")
        return

    playlist_name = click.prompt(f"What playlist to remove from", type=click.STRING)

    playlist_path = os.path.join(playlists_path, playlist_name)
    if not os.path.exists(playlist_path):
        click.echo(f"Playlist doesn't exist at {playlist_path}.")
        return

    with open(os.path.join(playlist_path, "songs.txt"), "r+") as file:
        lines = [line.strip() for line in file.readlines() if line.strip() != ""]
        while lines.count(name) > 0:
            lines.remove(lines[lines.index(name)])

        file.seek(0)
        file.truncate()
        file.write("\n".join(lines))
        file.close()

    click.echo(f"Removed {name} from {os.path.join(playlist_path, "songs.txt")}.")


@playlist.command()
@click.help_option('-h', '--help')
@click.argument("name")
def create(name: str) -> None:
    """Create a playlist"""

    playlists_path = get_playlists_dir()
    if not os.path.exists(playlists_path):
        click.echo(f"Playlists directory doesn't exist at {playlists_path}.")
        return

    os.mkdir(os.path.join(playlists_path, name))

    click.echo(f"Created playlist at {os.path.join(playlists_path, name)}.")

    with open(os.path.join(playlists_path, name, "songs.txt"), "w") as file:
        file.close()
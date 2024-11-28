import os
import shutil
import click

from src.util.constants import get_playlists_dir


@click.group()
@click.help_option('-h', '--help')
def playlist() -> None:
    """Rename, delete, list, and create playlists"""


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
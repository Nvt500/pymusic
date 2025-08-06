
# pymusic

A cli to download and play music written in python.

Wherever the executable is, there needs to be a ```songs``` folder and ```playlists``` folder.
Or you can run the ```init``` command to create them. 

```text
> pymusic init
```

It downloads music from YouTube using ```yt-dlp``` and can download individual songs or entire 
playlists as long as it's public.

# Installation

Either download the executable from the releases or build it yourself with something like 
```pyinstaller```.

Simply

```text
> pyinstaller src/pymusic.py --onefile --console
```

Or use ```--onedir``` to reduce start up time

```text
> pyinstaller src/pymusic.py --onedir --console
```

To isolate the build files into a single directory where ```executable``` is the directory 
name.

```text
> pyinstaller src/pymusic.py --onefile --console --distpath executable --workpath executable --specpath executable
```

Or use ```--onedir``` to reduce start up time

```text
> pyinstaller src/pymusic.py --onedir --console --distpath executable --workpath executable/build --specpath executable
```

You can also use the build scripts ```build_one_file.py``` or ```build_one_dir.py```.

# Usage

## Download

```text
Usage: pymusic download [OPTIONS] URL

  Download music from url

  URL is a url to a YouTube video or PUBLIC playlist. (wrap url in quotes if
  there is an & in the url at least on windows cmd)

Options:
  -h, --help              Show this message and exit.
  -r, --replace           Replace file if it already exists.
  -t, --to-playlist NAME  Name of playlist to download to.
  -n, --no-cookies        Do not download using cookies.
```

Downloads a song or playlist. Use ```--to-playlist``` to download a 
song or playlist to a specific playlist. It won't download songs again unless ```--replace``` 
is used then it will replace the already downloaded song. If the song's name changes on YouTube
you must either change the name manually in songs and in each playlist the song is in, or 
delete all instances of the name and song and then download it again with the new name. If the 
playlists name changes, just replace the name of the folder in ```playlists```. It also strips
all non-alphanumeric characters for song names since there was some trouble in testing where
there would be weird characters in the ```songs.txt```.

It will skip over private/hidden videos in a playlist, although it will show an error. 
It will also be unable to download videos that are restricted by the network or something else for whatever reason so it
may be best to download them somewhere else and transfer them.

### Cookies

When downloading you can get flagged as a bot. In order to prevent this the user must input their 
cookies into the `cookies.txt`.
- First, download the [**Get cookies.txt LOCALLY**](https://chromewebstore.google.com/detail/Get%20cookies.txt%20LOCALLY/cclelndahbckbenkjhflpdbgdldlbecc) extension (any other equivalent extension or tool can
   be used, all that matters is that the cookies are in the **Netscape** format)
- Second, go to YouTube and login
- Third, click on the extension, make sure the export format is **Netscape**, and click copy in the top right
- Lastly, simply paste into the `cookies.txt` file created with the `init` command

The good part is that you should only have to do this once and if you do get some sort of error relating to cookies
just replace the cookies with fresh ones.

## Play

```text
Usage: pymusic play [OPTIONS] COMMAND [ARGS]...

  Play music.

Options:
  -h, --help  Show this message and exit.

Commands:
  playlist  Play playlist
  select    Select a song or playlist to play.
  song      Play song
```

The music player uses ```pygame.mixer``` to pause, resume, change volume, and stop the song.

### Playlist

```text
Usage: pymusic play playlist [OPTIONS] NAME

  Play playlist

Options:
  -h, --help     Show this message and exit.
  -r, --random   Randomize playlist
```

Play a playlist either in order or shuffled.

### Song

```text
Usage: pymusic play song [OPTIONS] NAME

  Play song

Options:
  -h, --help    Show this message and exit.
  -r, --repeat  Repeat a song (forever)
```

Play a song.

### Select

```text
Usage: pymusic play select [OPTIONS] WHICH

  Select a song or playlist to play.

  WHICH can be:
      "song" - select a song
      "playlist" - select a playlist
      "from-playlist" - select a playlist then a song from that playlist

  "song" is the default.

Options:
  -h, --help                 Show this message and exit.
  --max-items INTEGER RANGE  Maximum number of items displayed per page
                             [1<=x<=10]
  -r, --random               Randomize playlist (only applies when WHICH is
                             "playlist")
```

Select a song from all songs, playlist from all playlists, or song from a playlist. Easier than
typing the entire song/playlist name if it has a super long name.

## Song

```text
Usage: pymusic song [OPTIONS] COMMAND [ARGS]...

  Rename, delete, and list songs

Options:
  -h, --help  Show this message and exit.

Commands:
  delete  Delete a song
  list    List songs
  rename  Rename a song
```

Basic functionality with songs.

## Playlist

```text
Usage: pymusic playlist [OPTIONS] COMMAND [ARGS]...

  Rename, delete, list, list songs, add to, remove from, and create playlists

Options:
  -h, --help  Show this message and exit.

Commands:
  add     Add a song to a playlist
  create  Create a playlist
  delete  Delete a playlist
  list    List playlists
  remove  Remove a song from a playlist
  rename  Rename a playlist
  songs   List songs from a playlist
```

Basic functionality with playlists.

# Docker Support

Docker probably won't work because ```pywinctl``` can't get the window name and it might not be 
able to access the local filesystem since it is enclosed. And I ain't doing all that. If you 
want to make it work you probably want to change some stuff to get started. The dockerfile 
builds fine though.

Line 4-6 in ```pymusic.py``` for some reason.
```python
from src.play.play import play
from src.download.download import download
from src.util.constants import get_songs_dir, get_playlists_dir
```
To
```python
from play.play import play
from download.download import download
from util.constants import get_songs_dir, get_playlists_dir
```

Line 10-11 in ```constants.py``` it gets the executable path so either hard code it or figure 
out how to do it dynamically.
```python
def get_executable_path() -> str:
    return os.path.dirname(sys.argv[0])
```


# pymusic

A cli to download and play music written in python.

Wherever the executable is, there needs to be a ```songs``` folder and ```playlists``` folder.
Or you can run the ```init``` command to create them. 

```text
> pymusic init
```

It downloads music from YouTube using ```pytubefix``` and can download individual songs or entire 
playlists as long as it is public.

# Usage

## Download

```text
Usage: pymusic download [OPTIONS] URL

  Download music from url

  URL is a url to a YouTube video or PUBLIC playlist. (wrap url in quotes if
  there is an & in the url at least on windows cmd)

Options:
  -h, --help                 Show this message and exit.
  -w, --with-out-oauth       Download without oauth.
  -r, --replace              Replace file if it already exists.
  -t, --to-playlist NAME     Name of playlist to download to.
  -s, --sync                 Turn off asynchronous downloading.
  -m, --max-workers INTEGER  Input into ThreadPoolExecutor when async.
                             [default: 5]
```

Downloads song or playlist asynchronously as default. Use ```--to-playlist``` to download a 
song or playlist to a specific playlist. It won't download songs again unless ```--replace``` 
is used then it will replace the already downloaded song. If the song's name changes on YouTube
you must either change the name manually in songs and in each playlist the song is in, or 
delete all instances of the name and song and then download it again with the new name. If the 
playlists name changes, just replace the name of the folder in ```playlists```. It also strips
all non-alphanumeric characters for song names since there was some trouble in testing where
there would be wierd characters in the ```songs.txt```.

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
Thus, it is kinda heavy so there is a low cpu mode where it simply plays the wav file with 
```winsound``` (only available on windows).

### Playlist

```text
Usage: pymusic play playlist [OPTIONS] NAME

  Play playlist

Options:
  -h, --help     Show this message and exit.
  -r, --random   Randomize playlist
  -l, --low-cpu  Stripped down music player to hopefully take up less
                 resources
```

Play a playlist either in order or shuffled.

### Song

```text
Usage: pymusic play song [OPTIONS] NAME

  Play song

Options:
  -h, --help     Show this message and exit.
  -l, --low-cpu  Stripped down music player to hopefully take up less
                 resources
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
                             [1<=x<=9]
  -r, --random               Randomize playlist (only applies when WHICH is
                             "playlist")
  -l, --low-cpu              Stripped down music player to hopefully take up
                             less resources
```

Select a song from all songs, playlist from all playlists, or song from a playlist. Easier than
typing the entire song/playlist name if it has a super long name.

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

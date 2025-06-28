# pymusic changelog

## 0.2.0 - 6-28-2025 - Bugfix & Quality of Life Changes

- Changed the dependency `pytubefix` to `yt-dlp` so downloading actually works now
  - This ```Error occurred: <YoutubeVideoID> This request was detected as a bot. Use `use_po_token=True` to view. See more details at https://github.com/JuanBindez/pytubefix/pull/209.```
    error needed a lot of work to fix and would require node to be installed so yt-dlp is now being used
  - Async is removed as it does not really work with yt-dlp as the playlist is downloaded in order and besides it's still fairly fast
  - Oauth is now in the form of cookies (more info on README)
- `.wav` files were taking up tens of megabytes which is absurd and due to converting `.mp4` to `.wav`. 
  Now it is converted to `.mp3` in order to save space and is about a tenth of the size
- Removed the low cpu option in the `play` command as it did not decrease the cpu or memory usage in my testing
  and only works with `.wav` and not `.mp3` files
- Changed the dependency `pygame` to `pygame-ce` as there was a bit of text showing for a deprecated module

## 0.1.1 - 4-28-2025 - Bugfix & Quality of Life Change

- Updated pytubefix to 8.13.1 because of this error:
  - ```Error occurred: <YoutubeVideoID> (lol) This request was detected as a bot. Use `use_po_token=True` to view. See more details at https://github.com/JuanBindez/pytubefix/pull/209.```
- Made volume not change between songs when playing a playlist

## 0.1.0 - 11-28-2024 - Pymusic Created

- pymusic was created...
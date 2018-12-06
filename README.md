# anYme-dl


anYme-dl is an anime downloader that downloads best quality episodes from [AnimeHeaven](http://animeheaven.eu/).

  - First enter the anime name
  - Select the desired anime from search results
  - Download whole anime, range of episodes or a single anime

# Requirements

  - Python 3.x
  - Selenium, Beautiful Soup, lxml (No need to manually download these modules, on first run program will automatically download them) 
  - Chrome installed on your system
  - Currently only working on windows machines

# Usage

Just copy the `anime_heaven_dowld.py` into your anime folder and it will automatically download the anime with their names. When running for first time it will download `chromedriver` and create a folder `Files` and install some modules if you don't have them installed.



## Development

Want to add something? Please mail me at `mldata.apoorv@gmail.com`.

Found an issue? Please raise an issue or you can mail me also.

## Todo

  - Add MAL integration for names of the file.
  - Store Data about anime and other settings.
  - Resume download from before.

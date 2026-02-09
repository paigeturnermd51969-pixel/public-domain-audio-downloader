# Public Domain Audio Downloader

## Disclaimer
This project is provided for educational and personal use only.
The script is intended to download audio only from videos that are in the public domain, or for which you have obtained the necessary rights or permissions from the copyright holder.

Downloading, distributing, or using copyrighted material without authorization may violate copyright laws in your jurisdiction.
The author of this repository does not endorse or condone the unauthorized downloading or distribution of copyrighted content and assumes no liability for any misuse of this software.

By using this project, you agree to take full responsibility for your actions and to comply with all applicable laws.

## About
This is a simple Python script that downloads the audio from each video in a YouTube playlist and then stores each file in a neatly structured format. To use, simply pass the URL of the the playlist you wish to download from as an argument.

<<<<<<< HEAD
## Requirments
- Python 3
- Chrome or a Chrome derivative browser
=======
## Requirements
- Python 3
- pip
- Chrome (or a Chrome derivative browser)
>>>>>>> f1fb11d (Adding save all files in a separate branch)

## Usage Instuctructions for those unfamiliar with Python
### Linux or MacOS
```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

```bash
python3 downloader.py "https://www.youtube.com/watch?v=FgXYzF5-Yiw&list=PLKH-YE4Goc7lZIe7l67TDDKURsRWWW0vc&index=1"
```

```bash
deactivate
```

## TODO
This script is far from perfect. Here is a list of some upcoming improvments.
<<<<<<< HEAD
- Clean up code
- Test if it actually works on Windows. 
- Handle correct song ordering in playlists > 99 songs
- Make it so that non-technical peeps can easily use (Docker Container? GUI?)
- Automatic updates
=======
- Strip colons from filenames
- Handle correct song ordering in playlists > 99 songs
- Test if it actually works on Windows.
- Automatic updates
- Clean up code
- Make it so that non-technical peeps can easily use (Docker Container? GUI?)
>>>>>>> f1fb11d (Adding save all files in a separate branch)
- Handle forbidden charactars in different filesystems https://stackoverflow.com/questions/1976007/what-characters-are-forbidden-in-windows-and-linux-directory-names
https://stackoverflow.com/questions/1976007/what-characters-are-forbidden-in-windows-and-linux-directory-names
- Allow user to specify prefered codec as CLI arg
- Add CLI arg to just download a single song
- add a CLI arg to force POSIX Portable Filename Character Set in filenames

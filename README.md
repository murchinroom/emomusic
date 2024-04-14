# emomusic

Music emotion recognition:

- input: mp3 file
- output: (valence, arousal)

> See also: [the valence-arousal model of emotion](https://en.wikipedia.org/wiki/Emotion_classification).

## Getting Started

### Docker (recommended)

```sh
# Clone
git clone https://github.com/murchinroom/emomusic.git
cd emomusic

# Build
docker build -t emomusic:v0.2.3 .

# Run
docker run --rm -p 8002:8002 emomusic:v0.2.3
```

Client:

```sh
$ curl http://localhost:8002/predictmp3 -F "file=@/home/foo/Zoltraak.mp3" -i

HTTP/1.1 200 OK
date: Sun, 14 Apr 2024 09:19:04 GMT
server: uvicorn
content-length: 59
content-type: application/json

{"arousal":0.4330291748046875,"valence":0.5694110989570618}
```

### Native

Prerequisites:

- `Python 3.9.19`
- Poetry: https://python-poetry.org
- `libsndfile1`
  - for Debian: `sudo apt-get install -y libsndfile1`
  - for openSUSE: `sudo yzpper in libsndfile1`
- Notice in many systems, you have to rebuild `libsndfile1` with additional dependencies to make it supports the mp3 format. 
  - [bastibe/libsndfile-binaries](https://github.com/bastibe/libsndfile-binaries) provides the pre-compiled libsndfile.so that overcomes this problem. You can download a version of the lib suitable for your system and architecture from the repo.
  - And replace the libsndfile lib with it: `sudo ln -sf /path/to/libsndfile-binaries/libsndfile_arm64.so /usr/lib64/libsndfile.so.1`. (The path to `libsndfile.so.1` is depended on your system & package manager, for example, debian puts it in `/usr/lib/aarch64-linux-gnu/`)

Poetry (recommended, tested with macOS Sonoma and openSUSE Tumbleweed.):

```sh
# Clone
git clone https://github.com/murchinroom/emomusic.git
cd emomusic

# IF YOUR python --version IS NOT Python 3.9.16:
#    EDIT pyproject.toml FIRST:
#        SET: python = "YOUR_PYTHON_VERSION"
# AND RUN: poetry lock --no-update

# Setup python venv
poetry install
poetry shell

# Run
cd emomusic
uvicorn main:app --port 8002
```

Or, PIP (not tested, and outdated, do not use it):

```sh
pip install --requirement requirements.txt
```

## API Docs

Start the service:

```sh
uvicorn main:app --port 8002

# or

docker run --rm -p 8002:8002 emomusic:v0.2.3
```

Browser open: `http://localhost:8002/docs`

- Click the `POST /predictmp3` tile;
- Click the `Try it out` button;
- Select a `*.mp3` music file;
- Click `Execute` to make a prediction.

(All developers should already know how to use these swagger docs, If you are not, ~~search the ducking web~~ ask the ducking ChatGPT with a copy of the content from the link (`/openapi.json`) below the title (`FastAPI`) at the top of the page.)

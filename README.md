# emomusic

Music emotion recognition:

- input: mp3 file
- output: (valence, arouse)

## Setup

Poetry (recommended):

```sh
poetry install
poetry shell
```

Or, PIP:

```sh
pip install --requirement requirements.txt
```

## Web API

```sh
uvicorn main:app --port 8000
```

Browser open: `http://localhost:8000/docs`


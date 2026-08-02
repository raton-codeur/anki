ENV ?= dev

all : .venv print
	@ ANKI_ENV=$(ENV) uv run src/main.py

add : .venv print
	@ ANKI_ENV=$(ENV) uv run src/main.py add

get : .venv print
	@ ANKI_ENV=$(ENV) uv run src/main.py get

print:
	@ printf "\033c"
	@ echo "--- script pour anki ---"

.venv :
	uv init --bare
	uv add requests pyperclip send2trash spotipy

clean :
	rm -rf .venv uv.lock pyproject.toml spotify_token.json
	find . -name __pycache__ -exec rm -rf {} +

.PHONY: all add get print clean

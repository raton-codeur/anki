all : .venv
	@ printf "\033c"
	@ echo "--- script pour anki ---"
	@ uv run src/main.py

add : .venv
	@ printf "\033c"
	@ echo "--- script pour anki ---"
	@ uv run src/main.py add

get : .venv
	@ printf "\033c"
	@ echo "--- script pour anki ---"
	@ uv run src/main.py get

.venv :
	uv init --bare
	uv add requests pyperclip send2trash spotipy

clean :
	rm -rf .venv uv.lock pyproject.toml spotify_token.json
	find . -name __pycache__ -exec rm -rf {} +

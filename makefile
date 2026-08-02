dev : .venv print
	@ uv run src/main.py --env dev

dev-add : .venv print
	@ uv run src/main.py --env dev --only add

dev-get : .venv print
	@ uv run src/main.py --env dev --only get

prod : .venv print
	@ uv run src/main.py --env prod

prod-add : .venv print
	@ uv run src/main.py --env prod --only add

prod-get : .venv print
	@ uv run src/main.py --env prod --only get

print:
	@ printf "\033c"
	@ echo "--- script pour anki ---"

.venv :
	uv init --bare
	uv add requests pyperclip send2trash spotipy

clean :
	rm -rf .venv uv.lock pyproject.toml spotify_token.json
	find . -name __pycache__ -exec rm -rf {} +

.PHONY: dev dev-add dev-get prod prod-add prod-get print clean

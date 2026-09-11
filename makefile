ENV ?= dev

add : .venv
	uv run --env-file .env.$(ENV) src/add.py

get : .venv
	uv run --env-file .env.$(ENV) src/get.py

.venv :
	uv init --bare
	uv add requests pyperclip send2trash

clean :
	rm -rf .venv uv.lock pyproject.toml spotify_token.json
	find . -name __pycache__ -exec rm -rf {} +

.PHONY: add get clean

all : .venv
	@ printf "\033c"
	@ echo "--- script pour anki ---"
	@ uv run src/main.py

.venv :
	uv init --bare
	uv add requests pyperclip send2trash

clean :
	rm -rf .venv uv.lock pyproject.toml
	find . -name __pycache__ -exec rm -rf {} +

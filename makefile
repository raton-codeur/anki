test : /Users/quentinhauuy/code/anki/venv
	@ source /Users/quentinhauuy/code/anki/venv/bin/activate && python3 src/main.py

/Users/quentinhauuy/code/anki/venv :
	python3 -m venv /Users/quentinhauuy/code/anki/venv && source /Users/quentinhauuy/code/anki/venv/bin/activate && pip install -r /Users/quentinhauuy/code/anki/requirements.txt

clean :
	rm -rf /Users/quentinhauuy/code/anki/venv src/__pycache__
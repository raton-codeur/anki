
all : /Users/quentinhauuy/code/anki/venv
	@ printf "\033c"
	@ /Users/quentinhauuy/code/anki/venv/bin/python /Users/quentinhauuy/code/anki/src/main.py

/Users/quentinhauuy/code/anki/venv :
	python3 -m venv /Users/quentinhauuy/code/anki/venv && /Users/quentinhauuy/code/anki/venv/bin/pip install -r /Users/quentinhauuy/code/anki/requirements.txt

clean :
	rm -rf /Users/quentinhauuy/code/anki/venv /Users/quentinhauuy/code/anki/src/__pycache__
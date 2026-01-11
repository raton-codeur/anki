test : venv
	@ source /Users/quentinhauuy/code/anki/venv/bin/activate && python3 src/main.py

venv :
	python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt

clean :
	rm -rf venv src/__pycache__

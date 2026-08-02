import sys
from check_param import check_param
from add import add
from get import get
from utils import open_input_in_vscode

run_add = True
run_get = True

if len(sys.argv) > 1:
    if sys.argv[1] == "add":
        run_get = False
    elif sys.argv[1] == "get":
        run_add = False

check_param()

if run_add:
    add()
if run_get:
    get()

open_input_in_vscode()

import argparse
import define
from check_param import check_param
from add import add
from get import get
from utils import open_input_in_vscode

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--only",
        choices=["add", "get"],
        default=None,
        help="action à exécuter",
    )

    parser.add_argument(
        "--env",
        choices=["dev", "prod"],
        default="dev",
        help="configuration à utiliser",
    )

    return parser.parse_args()

def what_to_run(only):
    run_add = True
    run_get = True

    if only == "add":
        run_get = False
    elif only == "get":
        run_add = False

    return run_add, run_get

def main():
    args = parse_arguments()

    define.setup(args.env)

    run_add, run_get = what_to_run(args.only)

    check_param()

    if run_add:
        add()
        
    if run_get:
        get()

    open_input_in_vscode()

if __name__ == "__main__":
    main()

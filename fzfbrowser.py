#!/usr/local/bin/python3.10
"""

This script is particularly useful for:

- An interactive alternative to STX's line filter.
- Document browsing, where each line is meaningful (e.g. maxims, lyrics, books, etc).


"""

import os
import subprocess
import sys
import io
import platform
import argparse

if platform.system() == "Darwin":
    fzf_location = "/opt/homebrew/bin/fzf"
    bat_location = "bat"
else:
    fzf_location = "/usr/bin/fzf"
    bat_location = "batcat"

argparse = argparse.ArgumentParser(
    prog="xaph's FZFR - Fuzzy Review / Content Browser",
    description="""Used for single documents. To be used together with FZFC (spanning multiple documents).""",
)
argparse.add_argument(
    "files", help="Browse through single or multiple files.", nargs="+", default=None
)
argparse.add_argument(
    "--folder",
    action="store_true",
    default=False,
    help="Filter for specific folders (otherwise filter for all files).",
)
argparse.add_argument(
    "--exclude-folders",
    default=None,
)
argparse.add_argument("--disable-copy", action="store_true", default=False)
args = argparse.parse_args()


def abbreviate_book_title(fp):
    fn = os.path.splitext(os.path.basename(fp))[0].upper()
    return "".join(i[0] for i in fn.split(" "))


def get_text_data(args) -> str:

    text_all: [str] = []

    for fp in args.files:
        fp_id = abbreviate_book_title(fp)
        with open(fp, "r", encoding="utf8") as f:
            text: [str] = [f"[[{fp_id}]] {l}" for l in f.readlines() if l.strip() != ""]
            text_all.extend(text)

    text_without_newlines: str = "".join(
        l for l in text_all if l.replace("\n", "").strip() != ""
    )

    return text_without_newlines


def pipe_data_into_fzf(piped_data):
    _sed_dot_to_newline = r"""sed "s/\. /\.\\n\\n/g" """
    _sed_dot_bold_to_newline = r"""sed "s/\.\*\* /\.\*\*\\n\\n/g" """
    opt_seds = "|".join([_sed_dot_to_newline, _sed_dot_bold_to_newline])

    # Word-boundary wrapping not available
    batcat_opts = "-l md --terminal-width 100 --color=always"

    if platform.system() == "Darwin":
        clipboard_handler = "pbcopy"
        attr_copy_ctrl_y = (
            f"""ctrl-y:execute-silent(echo {{}} | {clipboard_handler})+abort,"""
            f"""enter:execute-silent(echo {{}} | {clipboard_handler})+abort"""
        )
    else:
        clipboard_handler = "xclip -sel c"
        attr_copy_ctrl_y = (
            f"""ctrl-y:execute-silent(echo -n {{}} | {clipboard_handler})+abort,"""
            f"""enter:execute-silent(echo {{}} | {clipboard_handler})+abort"""
        )

    if args.disable_copy:
        _binder = []
    else:
        _binder = [
            "--bind",
            attr_copy_ctrl_y,
        ]

    call_string = [
        "--reverse",
        "--color",
        "fg:#bbccdd,fg+:#ddeeff,bg:#334455,preview-bg:#223344,border:#778899" "",
        *_binder,
        "--preview-window",
        "up:wrap:30%,70%,border-bottom,+{2}+3/3,~3",
        "--preview",
        # """echo {} | sed "s/'./'/g" | batcat -l md --color=always""",
        # """echo {} | tr '.' '\n' | batcat -l md --color=always""",
        # Newlines added for reading purposes, but copy ignores newlines. `fold` might actually be redundant, but leaving this here for now.
        rf"""echo {{}} | {opt_seds}  | fold -w 80 -s | {bat_location} {batcat_opts}""",
    ]

    output = subprocess.run(
        [fzf_location, *call_string],
        # stdin=piped_data.stdout,
        input=piped_data,
    )


if args.files:
    for file in args.files:
        if not os.path.exists(file):
            print(f"Filepath does not exist: {os.path.basename(args.file)}")
            sys.exit()


if __name__ == "__main__":
    text = get_text_data(args)
    pipe_data_into_fzf(text.encode())

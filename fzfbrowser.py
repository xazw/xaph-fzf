#!/usr/local/bin/python3.10

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
argparse.add_argument("file", help="Single file to read")
argparse.add_argument("--disable-copy", action="store_true", default=False)
args = argparse.parse_args()


def get_text_data(args) -> str:

    with open(args.file, "r", encoding="utf8") as f:
        text = f.readlines()

    text_without_newlines: str = "".join(
        l for l in text if l.replace("\n", "").strip() != ""
    )

    return text_without_newlines


def pipe_data_into_fzf(piped_data):
    _sed_dot_to_newline = r"""sed "s/\. /\.\\n\\n/g" """
    _sed_dot_bold_to_newline = r"""sed "s/\.\*\* /\.\*\*\\n\\n/g" """
    opt_seds = "|".join([_sed_dot_to_newline, _sed_dot_bold_to_newline])
    batcat_opts = "-l md --terminal-width 100 --color=always"

    if args.disable_copy:
        _binder = []
    else:
        _binder = ["--bind", """enter:execute-silent(echo {} | xclip -sel c)+abort"""]

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
        rf"""echo {{}} | {opt_seds}  | fold -w 80 -s | {bat_location} {batcat_opts}""",  # Newlines added for reading purposes, but copy ignores newlines
    ]

    output = subprocess.run(
        [fzf_location, *call_string],
        # stdin=piped_data.stdout,
        input=piped_data,
    )


if args.file:
    if not os.path.exists(args.file):
        print(f"Filepath does not exist: {os.path.basename(args.file)}")
        sys.exit()


if __name__ == "__main__":
    text = get_text_data(args)
    pipe_data_into_fzf(text.encode())

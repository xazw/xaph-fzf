#!/usr/local/bin/python3.10
"""
xaph's FZFR Content Browser
- Used for single documents.
- To be used together with FZFC (spanning multiple documents)

Usage:
-f <file> | --file <file> : File to read
-h | --help : Show this help message

"""

import os
import subprocess
import sys
import io
import platform

try:
    sys.argv[1]
except:
    print(__doc__)
    sys.exit(1)

match sys.argv[1]:
    case "-h" | "--help":
        # help_title = "HELP"
        # print(f"{help_title:-^20}")
        print(__doc__)
        sys.exit(1)
    case "-f" | "--file":
        try:
            filepath = sys.argv[2]
            if not os.path.exists(filepath):
                print(f"Filepath does not exist: {os.path.basename(filepath)}")
                print(sys.argv)
                sys.exit()
        except Exception as err:
            print(f"Error: {err}")
            sys.exit(1)
    case _:
        print(f"No TXT/MD file provided.")
        print(__doc__)
        sys.exit(1)


def get_text_data() -> (subprocess.Popen, str):
    """Currently, it reads both via Python and via cat. I should remove the redundancy later."""

    text_filepath = filepath
    with open(text_filepath, "r", encoding="utf8") as f:
        text = f.readlines()
    text_without_newlines: str = "\n".join([l for l in text if l.strip() != ""])

    cat_popen = subprocess.Popen(
        ["cat", text_filepath],
        stdout=subprocess.PIPE,
    )
    return cat_popen, text_without_newlines


def filter_text_data(piped_data: subprocess.Popen, data: str) -> bytes:

    # Remove newlines from input
    p = subprocess.Popen(
        # ["grep", "-v", "^$"], # If grep-based inverted-newline removal is needed, but no longer since we're using Python
        ["grep", "."],  # grep matches everything
        stdin=subprocess.PIPE,  # ALT: stdin=piped_data.stdout,
        stdout=subprocess.PIPE,
    )
    out = p.communicate(data.encode())

    return out[0]  # .decode()

if platform.system() == "Darwin":
    fzf_location = "/opt/homebrew/bin/fzf"
    bat_location = "bat"
else:
    fzf_location = "/usr/bin/fzf"
    bat_location = "batcat"

sed_dot_to_newline = r"""sed "s/\. /\.\\n\\n/g" """
sed_dot_bold_to_newline = r"""sed "s/\.\*\* /\.\*\*\\n\\n/g" """

opt_seds = "|".join([sed_dot_to_newline, sed_dot_bold_to_newline])
batcat_opts = "-l md --terminal-width 100 --color=always"




def pipe_data_into_fzf(piped_data):
    output = subprocess.run(
        [
            fzf_location,
            "--reverse",
            "--color",
            # "fg:#bbccdd,fg+:#ddeeff,bg:#334455,preview-bg:#223344,border:#778899""",
            # "preview-bg:#223344,border:#778899""",
            "--bind",
            """enter:execute-silent(echo {} | xclip -sel c)+abort""",
            "--preview-window",
            "up:wrap:30%,70%,border-bottom,+{2}+3/3,~3",
            "--preview",
            # """echo {} | sed "s/'./'/g" | batcat -l md --color=always""",
            # """echo {} | tr '.' '\n' | batcat -l md --color=always""",
            rf"""echo {{}} | {opt_seds}  | fold -w 80 -s | {bat_location} {batcat_opts}""",  # Newlines added for reading purposes, but copy ignores newlines
        ],
        # stdin=piped_data.stdout,
        input=piped_data,
    )


if __name__ == "__main__":
    cat, text = get_text_data()
    text_delined = filter_text_data(cat, text)
    pipe_data_into_fzf(text_delined)
    # cat.wait()

# TODO: Enable colorized preview

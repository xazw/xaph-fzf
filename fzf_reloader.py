#!/usr/bin/python3

import argparse
import os
import re
import time
import platform

# import pyperclip

XAPH_FS_FILES = "~/.xaph-fs"
XAPH_FS_FOLDERS = "~/.xaph-fsd"
DEFAULT_MAC_SEARCH_FOLDER = "/Users/xaph"
DEFAULT_LINUX_SEARCH_FOLDER = "$HOME"

time_start = time.time()
parser = argparse.ArgumentParser(prog="XAPH-FZF")
parser.add_argument(
    "--folder",
    action="store_true",
    default=False,
    help="Filter for folders (otherwise search only files)",
)
parser.add_argument(
    "--write",
    action="store_true",
    default=False,
    help="Write reload to disk",
)
parser.add_argument(
    "--multi",
    action="store_true",
    default=False,
    help="Allow multiple selections",
)
parser.add_argument(
    "--specific-location",
    help="Filter for files (not folders) within specific locations",
    # NOTE: I will not support looking for a specific folder within folders, not necessary
)

args = parser.parse_args()
# pyperclip.copy(f"{args.folder=} {args=}")


if args.specific_location:
    folder_to_search = args.specific_location
else:
    if platform.system() == "Darwin":
        folder_to_search = DEFAULT_MAC_SEARCH_FOLDER
    else:
        folder_to_search = DEFAULT_LINUX_SEARCH_FOLDER


if platform.system() == "Darwin":
    fd = "fd"
    clipboard_handler = "pbcopy"
    exclude_folders = ["-E 'venv-*'", "-E '/Library/*'"]
    SEARCH_STRING = fd + f"  . {folder_to_search} -I " + " ".join(exclude_folders)
    SEARCH_STRING_FOLDER = (
        fd + " -t d" + f" . {folder_to_search} -I " + " ".join(exclude_folders)
    )
else:
    fd = "fdfind"
    clipboard_handler = "xclip -sel c"
    exclude_folders = ["-E 'venv-*'"]
    SEARCH_STRING = (
        fd + f"  . {folder_to_search} -I " + " ".join(exclude_folders) + " --follow"
    )
    SEARCH_STRING_FOLDER = (
        fd
        + " -t d"
        + f"  . {folder_to_search} -I "
        + " ".join(exclude_folders)
        + "--follow"
    )


def update_cache(
    message: str = "Update",
    dump_to_fzf=False,
    folder=True,
    location=None,
    search_string=SEARCH_STRING,
    search_string_folder=SEARCH_STRING_FOLDER,
):
    """

    :param message:
    :param dump_to_fzf: If true, then print to FZF, instead of saving to disk
    :param folder: Whether to search for folders or files
    :param location: Specific location to use for search, in tandem with args.specific_location
    :param search_string: For files, replaceable by location
    :param search_string_folder: For folders, replaceable by location
    :return:
    """

    time_cache_start = time.time()

    if not dump_to_fzf:
        if folder:
            print(
                f"{message} at {XAPH_FS_FOLDERS}... {location if location else 'Default location'}"
            )
        else:
            print(
                f"{message} at {XAPH_FS_FILES}... {location if location else 'Default location'}"
            )

    if location:
        # Assume provided location is correct (regardless of platform),
        # because the script won't load in the first place if the location is incorrect
        search_string = re.sub(folder_to_search, location, search_string)
        search_string_folder = re.sub(folder_to_search, location, search_string_folder)

    if folder and dump_to_fzf:
        os.system(search_string_folder)
    elif folder and (dump_to_fzf is False):
        os.system(f"{search_string_folder} > {XAPH_FS_FOLDERS}")
    elif (folder is False) and dump_to_fzf:
        os.system(search_string)
    elif (folder is False) and (dump_to_fzf is False):
        os.system(f"{search_string} > {XAPH_FS_FILES}")

    if not dump_to_fzf:
        print(f"Time to update cache: {(time.time() - time_cache_start):.2f}s\n")


_pipe = " | "
_fzf_fs_open_files = f"cat {XAPH_FS_FILES}"
_fzf_fs_open_folders = f"cat {XAPH_FS_FOLDERS}"
_fzf_header = f"fzf --header 'Search FILES via {fd}'"
_fzf_header_folders = f"fzf --header 'Search FOLDERS via {fd}'"
_reverse_binder = " --reverse --bind"
_base_common_summons = _fzf_fs_open_files + _pipe + _fzf_header + _reverse_binder
_base_common_summons_folders = (
    _fzf_fs_open_folders + _pipe + _fzf_header_folders + _reverse_binder
)


attr_enter_linux = (
    f"""enter:execute-silent(setsid xdg-open {{}} &)"""
    + ("" if args.multi else "+abort")
    + ","
)
attr_enter_mac = (
    """enter:execute(open {} > /dev/null 2>&1)"""
    + ("" if args.multi else "+abort")
    + ","
)

attr_copy_linux = (
    f"""ctrl-y:execute-silent(echo -n {{}} | {clipboard_handler})+abort,"""
)
attr_copy_mac = """ctrl-y:execute-silent(echo {} | pbcopy)+abort,"""
attr_copy_folder_mac = """alt-c:execute-silent(echo `basename {}` | pbcopy)+abort,"""
attr_copy_folder_linux = (
    f"""alt-c:execute-silent(echo -n `basename {{}}` | {clipboard_handler})+abort,"""
)
# attr_del_mac = f"""del:execute(rm -f {{}})+reload({fd} . /Users/xaph),"""
attr_open_folder_linux = (
    f"""ctrl-h:execute-silent(setsid xdg-open "`dirname {{}}`" | {clipboard_handler})"""
    + ("" if args.multi else "+abort")
    + ","
)
attr_open_folder_mac = (
    """ctrl-h:execute-silent(open "`dirname {}`" | pbcopy)"""
    + ("" if args.multi else "+abort")
    + ","
)

if args.specific_location:
    _loc = f' --specific-location "{args.specific_location}"'
else:
    _loc = ""

attr_reload_linux = f"""ctrl-r:reload(/usr/bin/python3 /home/xaph/Dropbox/arcanum/grimoire/common/fzf/fzf_reloader.py{_loc} --write),"""
attr_reload_folders_linux = f"""ctrl-r:reload(/usr/bin/python3 /home/xaph/Dropbox/arcanum/grimoire/common/fzf/fzf_reloader.py  --folder{_loc} --write),"""
attr_reload_mac = f"""ctrl-r:reload(/usr/bin/python3 /Users/xaph/Dropbox/arcanum/grimoire/common/fzf/fzf_reloader.py{_loc} --write),"""
attr_reload_folders_mac = f"""ctrl-r:reload(/usr/bin/python3 /Users/xaph/Dropbox/arcanum/grimoire/common/fzf/fzf_reloader.py  --folder{_loc}),"""
attr_common_shift_page = (
    """shift-up:preview-half-page-up,shift-down:preview-half-page-down"""
)
attr_common_preview_window = (
    """--preview-window  'down:wrap:40%,40%,border-bottom,+{2}+3/3,~3'"""
)
attr_common_preview_opts_linux = (
    ''' --preview "batcat --color=always `echo '{}' | sed "s/'/\\\'/g"`"'''
)
attr_common_preview_opts_mac = (
    ''' --preview "bat --color=always `echo '{}' | sed "s/'/\\\'/g"`"'''
)

if __name__ == "__main__":
    # This section is only called if doing reloads from within FZF itself.
    if args.folder:
        if args.write:
            update_cache(dump_to_fzf=False, folder=True)
        update_cache(dump_to_fzf=True, folder=False)
    else:
        if args.write:
            update_cache(dump_to_fzf=False, folder=False)
        update_cache(dump_to_fzf=True, folder=False)

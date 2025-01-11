#!/usr/bin/python3

"""
- This script is meant for launching with Ulauncher, Alfred, i3, or a CLI terminal.
- It is not meant for cron-scripts or reloads within FZF.
- Use 'fzfs' (location-specific shorthand) compared to the general launcher as need be.

- Script is VERY tightly coupled to the reloader; this is intentional, and specific to  this script.
  It calls to various parts of the reloader outside of its main() function.


"""


import os
import platform
import subprocess
import sys
import time

from settings import (
    args,
    XAPH_FS_FOLDERS,
    XAPH_FS_FILES,
    DEFAULT_LINUX_SEARCH_FOLDER,
    DEFAULT_MAC_SEARCH_FOLDER,
)

from fzf_reloader import (
    update_cache,
    _base_common_summons,
    _base_common_summons_folders,
    attr_copy_folder_mac,
    attr_open_folder_mac,
    # attr_del_mac,
    attr_common_preview_opts_linux,
    attr_common_preview_opts_mac,
    attr_enter_linux,
    attr_enter_mac,
    attr_copy_linux,
    attr_copy_mac,
    attr_copy_folder_linux,
    attr_open_folder_linux,
    attr_reload_linux,
    attr_reload_mac,
    attr_reload_folders_linux,
    attr_reload_folders_mac,
    attr_common_shift_page,
    attr_common_preview_window,
)


def create_things(created_folders, created_files):
    if created_folders:
        # threading.Thread(
        #     target=update_cache,
        #     kwargs={"print_to_fzf": False, "folder": True, "location": folder_to_search},
        # ).start()
        update_cache(
            print_to_fzf=False,
            folder=True,
            location=folder_to_search,
        )

    if created_files:
        # threading.Thread(
        # target=update_cache,
        # kwargs={
        # "print_to_fzf": False,
        # "folder": False,
        # "location": folder_to_search,
        # },
        # ).start()
        update_cache(
            print_to_fzf=False,
            folder=False,
            location=folder_to_search,
        )
        # os.system('python -c /home/xaph/Dropbox/arcanum/grimoire/common/fzf/fzf_reloader.py')


if __name__ == "__main__":
    time_start = time.time()

    created_folders = False
    created_files = False

    if args.specific_location:
        if not os.path.exists(args.specific_location):
            sys.exit(f"Folder does not exist: {args.specific_location}")

    if args.folder:
        if args.specific_location:
            update_cache(
                "Create specific",
                print_to_fzf=False,
                folder=True,
                location=args.specific_location,
            )
            created_folders = True
        elif os.path.exists(os.path.expanduser(XAPH_FS_FOLDERS)):
            created_folders = True
        else:
            update_cache("Update FZF with folder cache", print_to_fzf=True, folder=True)

    else:
        if args.specific_location:
            update_cache(
                "Create specific",
                print_to_fzf=False,
                folder=False,
                location=args.specific_location,
            )
            created_files = True
        elif os.path.exists(os.path.expanduser(XAPH_FS_FILES)):
            created_files = True
        else:
            update_cache("Update FZF with files cache", print_to_fzf=True, folder=False)

    if platform.system() == "Darwin":
        combined_string = (
            (_base_common_summons if not args.folder else _base_common_summons_folders)
            + " '"
            + attr_enter_mac
            + attr_copy_mac
            + attr_copy_folder_mac
            + attr_open_folder_mac
            # + attr_del_mac
            + (attr_reload_mac if not args.folder else attr_reload_folders_mac)
            + attr_common_shift_page
            + "' "
            + attr_common_preview_window
            + attr_common_preview_opts_mac
        )
    else:
        combined_string = (
            (_base_common_summons if not args.folder else _base_common_summons_folders)
            + " '"
            + attr_enter_linux
            + attr_copy_linux
            + attr_copy_folder_linux
            + attr_open_folder_linux
            + (attr_reload_linux if not args.folder else attr_reload_folders_linux)
            + attr_common_shift_page
            + "' "
            + attr_common_preview_window
            + attr_common_preview_opts_linux
        )

    print(f"CMD: '{combined_string}'\n")

    subprocess.run(
        combined_string, shell=True
    )  # No need to use threading.Thread(target=os.system, args=[combined_string]).start()

    if args.specific_location is not None:
        if platform.system() == "Darwin":
            folder_to_search = DEFAULT_MAC_SEARCH_FOLDER
        else:
            folder_to_search = DEFAULT_LINUX_SEARCH_FOLDER

        print(f"Restoring from {args.specific_location} to {folder_to_search}...")
    else:
        folder_to_search = None

    if args.write:
        create_things(created_folders, created_files)

    print(f"Time in XAPH-FZF: {(time.time() - time_start):.2f}s\n")

import argparse

parser = argparse.ArgumentParser(
    prog="xaph-FZF",
    description="A command-line utility for filtering and searching files or folders interactively using FZF.",
)
parser.add_argument(
    "--specific-location",
    help="Filter for files (not folders) within specific locations",
    # NOTE: I will not support looking for a specific folder within folders, not necessary
)
parser.add_argument(
    "--folder",
    action="store_true",
    default=False,
    help="Filter for specific folders (otherwise filter for all files).",
)
parser.add_argument(
    "--exclude-folders",
    default=None,
)
parser.add_argument(
    "--write",
    action="store_true",
    default=False,
    help="Write reloads to disk (otherwise only print to terminal/FZF).",
)
parser.add_argument(
    "--multi",
    action="store_true",
    default=False,
    help="Execute without closing window/i.e. multi-selection.",
)
parser.add_argument(
    "--fdcron",
    action="store_true",
    default=False,
    help="Different alias for running fd via crontab (Mac-specific cron-usage).",
)

args = parser.parse_args()

XAPH_FS_FILES = "~/.xaph-fs"
XAPH_FS_FOLDERS = "~/.xaph-fsd"
DEFAULT_MAC_SEARCH_FOLDER = "/Users/xaph"
DEFAULT_LINUX_SEARCH_FOLDER = "$HOME"

# XAPH-2022-08-13 17:56:51
# Passing parameters to a Bash function - https://stackoverflow.com/a/6212408/283169

OS=$(uname -s)


if [ "$OS" = 'Darwin' ]; then

    _fzf() {
         /Users/xaph/Dropbox/arcanum/grimoire/common/ripgrep/axii-rg-list-all-files-in-folder.sh | fzf --header 'Search text content in files' --reverse --ansi --disabled --bind 'enter:execute(open {} > /dev/null 2>&1),ctrl-y:execute-silent(echo {} | pbcopy),alt-c:execute-silent(echo `basename {}` | pbcopy),ctrl-h:execute-silent(open "`dirname {}`" | pbcopy),change:reload(/Users/xaph/Dropbox/arcanum/grimoire/common/ripgrep/axii-rg-list-all-files-in-folder.sh {q} || true),shift-up:preview-half-page-up,shift-down:preview-half-page-down' --preview-window 'right:wrap:40%,60%,border-bottom,+{2}+3/3,~3' --preview "bat --color=always `echo '{}' | sed "s/'/\\\'/g"`"
            # "`printf %q {}`"
            # `printf %q {q}` - WORKS
            # `echo '{}' | sed "s/'/\\\'/g"` - WORKS
            # --preview "batcat --color=always --highlight-line :20 `echo '{}' | sed "s/'/\\\'/g"`" - WORKS
     };


    # See 3. Interactive ripgrep integration

    # --disabled - "...we used --disabled option so that fzf doesn't perform any secondary filtering."
    # - If not for the above, then fzf filters by file name as well, on top of contents.
    # The ``|| true` suppresses the error message

    _fzf "$1"

    # For quoting using batcat
    # https://stackoverflow.com/a/11514818/283169


else

    # sh /home/xaph/Dropbox/arcanum/grimoire/common/trash/clean_all_unnecessaries.sh;

    _fzf() {
         /home/xaph/Dropbox/arcanum/grimoire/common/ripgrep/axii-rg-list-all-files-in-folder.sh | fzf --header 'Search text content in files' --reverse --ansi --disabled --bind 'enter:execute(xdg-open {} > /dev/null 2>&1),ctrl-y:execute-silent(echo -n {} | xclip -sel c),alt-c:execute-silent(echo -n `basename {}` | xclip -sel c),ctrl-h:execute-silent(nautilus "`dirname {}`" | xclip -sel c),change:reload(/home/xaph/Dropbox/arcanum/grimoire/common/ripgrep/axii-rg-list-all-files-in-folder.sh {q} || true),shift-up:preview-half-page-up,shift-down:preview-half-page-down,ctrl-f:page-down,ctrl-b:page-up' --preview-window 'down:wrap:20%,80%,border-top,+{2}+3/3,~3' --preview "batcat --terminal-width 80 --color=always `echo '{}' | sed "s/'/\\\'/g"` "
         # /home/xaph/Dropbox/arcanum/grimoire/common/ripgrep/axii-rg-list-all-files-in-folder.sh | fzf --header 'Search text content in files' --reverse --ansi --disabled --bind 'enter:execute(xdg-open {} > /dev/null 2>&1),ctrl-y:execute-silent(echo {} | xclip -sel c),alt-c:execute-silent(echo `basename {}` | xclip -sel c),ctrl-h:execute-silent(nautilus "`dirname {}`" | xclip -sel c),change:reload(/home/xaph/Dropbox/arcanum/grimoire/common/ripgrep/axii-rg-list-all-files-in-folder.sh {q} || true),shift-up:preview-half-page-up,shift-down:preview-half-page-down' --preview-window 'right:wrap:40%,60%,border-bottom,+{2}+3/3,~3' --preview "batcat --color=always `echo '{}' | sed "s/'/\\\'/g"`"
            # "`printf %q {}`"
            # `printf %q {q}` - WORKS
            # `echo '{}' | sed "s/'/\\\'/g"` - WORKS
            # --preview "batcat --color=always --highlight-line :20 `echo '{}' | sed "s/'/\\\'/g"`" - WORKS
     };


    # See 3. Interactive ripgrep integration

    # --disabled - "...we used --disabled option so that fzf doesn't perform any secondary filtering."
    # - If not for the above, then fzf filters by file name as well, on top of contents.
    # The ``|| true` suppresses the error message

    _fzf "$1"

    # For quoting using batcat
    # https://stackoverflow.com/a/11514818/283169


fi


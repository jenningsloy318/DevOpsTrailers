ssh() {
    if [ "$(ps -p $(ps -p $$ -o ppid=) -o comm=)" = "tmux" ]; then
            tmux rename-window "$*"
            command ssh "$@"
            tmux set-window-option automatic-rename "on" 1>/dev/null
    else
            command ssh "$@"
    fi
}
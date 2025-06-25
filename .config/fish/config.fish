# Command
if status is-interactive
    starship init fish | source
end

# Variables
set -x VISUAL $EDITOR
set -x EDITOR nvim
set -x TERMINAL kitty
set -x BROWSER zen-browser
set -x FILE_MANAGER thunar
set -x HISTORY_IGNORE '(ls|cd|pwd|exit|sudo reboot|history|cd -|cd ..)'

set -x PATH $HOME/.deno/bin $PATH
set -x SDL_VIDEODRIVER wayland
set -x PYTHONPYCACHEPREFIX ~/.cache/__pycache__
set -x MYPY_CACHE_DIR ~/.cache/.mypy_cache
set -x WAYLAND_DISPLAY wayland-1
set -x XDG_SESSION_TYPE wayland
set -x SDL_VIDEO_DRIVER wayland
set -x DISPLAY $DISPLAY

# Alias
alias mirrors="sudo reflector --verbose --latest 5 --country 'United States' --age 6 --sort rate --save /etc/pacman.d/mirrorlist"
alias grub-update="sudo grub-mkconfig -o /boot/grub/grub.cfg"
alias manten="yay -Sc; and sudo pacman -Scc"
alias purga="sudo pacman -Rns (pacman -Qtdq); and sudo fstrim -av"
alias update="paru -Syu --nocombinedupgrade"
alias vm-on="sudo systemctl start libvirtd.service"
alias vm-off="sudo systemctl stop libvirtd.service"
alias music="ncmpcpp"
alias ls="lsd -a --group-directories-first"
alias ll="lsd -la --group-directories-first"
alias pk="pkexec"
alias pkill="pkill -f"
alias cp="cp -r"
alias x+="xhost +SI:localuser:root"
alias x-="xhost -SI:localuser:root"

# Fuction and Dir
function dir_icon
    if test $PWD = $HOME
        echo -n (set_color cyan)'󱂵'(set_color normal)
    else
        echo -n (set_color cyan)''(set_color normal)
    end
end

function fish_prompt
    set_color blue; echo -n ' '; set_color normal
    set_color magenta; echo -n (whoami) ''; set_color normal
    dir_icon
    #set_color red; echo -n " " (prompt_pwd) " "; set_color normal #Short
    set_color red; echo -n " "(string replace -r "^$HOME" "~" $PWD)" "; set_color normal #Normal
    if test $status -eq 0
        set_color green; echo -n ' '; set_color normal
    else
        set_color red; echo -n ' '; set_color normal
    end
end

function expand_or_complete_with_dots
    echo -n (set_color red)'…'(set_color normal)
    commandline -f complete
end

bind \t expand_or_complete_with_dots

function save_last_dir --on-event fish_exit
    pwd > ~/.lastdir
end

if test -f ~/.lastdir
    cd (cat ~/.lastdir)
end

set fish_greeting

set -x PATH $HOME/.local/bin $PATH

set -gx SHELL /sbin/fish

~/.local/bin/colorscript -r

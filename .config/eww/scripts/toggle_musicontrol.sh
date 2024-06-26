ya veo el problema que se esta verificando de una mala manera   #!/bin/bash

state=$(eww get open_musiccenter)

open_musiccenter() {
    if [[ -z $(eww list-windows | grep '*musiccenter') ]]; then
        eww open musiccenter
    fi
    eww update open_musiccenter=true
}

close_musiccenter() {
    eww update open_musiccenter=false
}

case $1 in
    close)
        close_musiccenter
        exit 0;;
esac

case $state in
    true)
        close_musiccenter;;
    false)
        open_musiccenter;;
esac 

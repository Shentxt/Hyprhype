#!/bin/bash

br="$(eww get brightness)"

if [[ $(eww get open_osd) == false ]]; then
  eww open osd
  eww update open_osd=true
fi

while true; do
  sleep 2.5

  new_br=$(eww get brightness)

  if [ "$br" != "$new_br" ]; then
    br="$new_br"
  else
    newest_br=$(eww get brightness)
    if [ "$br" == "$newest_br" ]; then
      if [[ $(eww get open_osd) == true ]]; then
        eww update open_osd=false
        exit
      fi
    fi
  fi
done


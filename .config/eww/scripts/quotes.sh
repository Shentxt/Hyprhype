#!/bin/bash

# personalized quotes
quote_file="$HOME/.config/quotes/quotes.json"

updatequotes() {
	local quote_file="$1"

	# Quotes api
	# uri=$(curl -s "https://api.quotable.io/random?maxLength=110")
	# echo $uri | jq '.content' | cut -d "\"" -f 2 >"$HOME/.cache/eww.quote"
	# echo $uri | jq '.author' | cut -d "\"" -f 2 >"$HOME/.cache/eww.author"
}

get_quote_and_author() {
	local selected_quote
	local selected_author

	selected_quote_author=$(jq -r '.[] | select(.quote, .author) | "\(.quote) - \(.author)"' "$quote_file" | shuf -n 1)
	selected_quote=$(echo "$selected_quote_author" | awk -F ' - ' '{print $1 "\""}')
	selected_author=$(echo "$selected_quote_author" | awk -F ' - ' '{print "- " $2}')

	selected_quote=$(echo "$selected_quote" | fold -s -w 60)

	echo "$selected_quote"
	echo "$selected_author"
}

# read the quotes
# quote=$(cat $HOME/.cache/eww.quote)

# read the authors
# author=$(cat $HOME/.cache/eww.author)

case $1 in
quote)
	# echo "$quote"
	get_quote_and_author
	;;
author)
	# echo "-$author"
	;;
update)
	# updatequotes "$quotes"
	updatequotes "$quote_file"
	;;
esac

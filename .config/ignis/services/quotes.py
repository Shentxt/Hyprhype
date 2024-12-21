import json
import os
import random

quote_file = os.path.expanduser("~/.config/quotes/quotes.json")

def updatequotes(quote_file):
    pass  

def get_quote_and_author(quote_file):
    with open(quote_file, "r") as file:
        quotes = json.load(file)
    
    selected_quote_author = random.choice(quotes)
    selected_quote = selected_quote_author["quote"]
    selected_author = selected_quote_author["author"]
    
    formatted_quote = "\n".join(selected_quote[i:i+60] for i in range(0, len(selected_quote), 60))
    
    return formatted_quote, selected_author

def main(action):
    if action == "quote":
        quote, author = get_quote_and_author(quote_file)
        print(f"{quote}\n- {author}")
    elif action == "author":
        pass  
    elif action == "update":
        updatequotes(quote_file)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: python script.py [quote|author|update]")

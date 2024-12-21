from ignis.widgets import Widget
from services.quotes import get_quote_and_author, quote_file

def quotes_widget():
    quote_text, quote_author = get_quote_and_author(quote_file)

    return Widget.Box(
        css_classes=["one"],
        vexpand=False,
        hexpand=True,
        child=[
            Widget.Box(
                css_classes=["quote"],
                vertical=True,
                child=[
                    Widget.Label(
                        css_classes=["quote-text"],
                        label=f"\"{quote_text}\""
                    ),
                    Widget.Label(
                        css_classes=["quote-text"],
                        label=quote_author
                    )
                ]
            )
        ]
    )

class NewsTemplate:
    title = "**{title}**"
    image = "[image]({image})"
    footer = (
"""
----

^^contribute: [^^source](https://github.com/pykancha/reddit-bots)
"""

    )

    tldr = (
"""
Tl;dr version:

{title}

{image}

{tldr}

{footer}
"""
)

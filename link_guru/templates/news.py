class NewsTemplate:
    title = "**{title}**"
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

[Article Link]({link})

{tldr}

{footer}
"""
)

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

{image} [Article Link]({link})

{tldr}

{footer}
"""
)

    summary = (
"""
Summary of the news:
        
{title}

{image} [Article Link]({link})

{news}

{footer}
"""
)

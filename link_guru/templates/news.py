class NewsTemplate:
    title = "**{title}**"
    image = "[image]({image})"
    date = "Date: {date}"
    translation = "*See reply of this comment for English translation:*"

    framework = (
"""
Summary of the news linked:

{translation_info}

{title}

{date}  {image}

{text}

----

^^contribute: [^^source](https://github.com/pykancha/reddit-bots)
"""
)

    framework_en = (
"""
{title}

{date}  {image}

{text}
"""
)

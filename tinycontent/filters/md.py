import markdown


def markdown_filter(content):
    return markdown.markdown(
        content,
        extensions=['nl2br', ]
    )

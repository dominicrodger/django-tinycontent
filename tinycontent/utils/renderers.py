import markdown


def markdown_renderer(content):
    return markdown.markdown(
        content,
        extensions=['nl2br', ]
    )

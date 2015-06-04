from tinycontent.utils.file_uploads import get_fileuploads


def uploaded_file_filter(content):
    for match in get_fileuploads(content):
        link = (
            '<a href="%s">Download %s</a>'
            % (match.file.file.url, match.file.name)
        )
        content = content.replace(match.full, link)

    return content

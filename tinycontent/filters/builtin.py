from tinycontent.utils.file_uploads import get_fileuploads


def uploaded_file_filter(content):
    for match in get_fileuploads(content):
        content = content.replace(match.full, match.file.file.url)

    return content

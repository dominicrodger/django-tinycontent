import re
from tinycontent.models import TinyContentFileUpload


fileupload_expression = re.compile(r'(@file:([A-Za-z0-9\-_]+))')


class FileMatch(object):
    def __init__(self, match):
        self.full = match[0]
        self.fileupload = TinyContentFileUpload.objects.get(
            slug=match[1]
        )

    def tag(self):
        url = self.fileupload.file.url
        name = self.fileupload.name
        return '<a href="%s">Download %s</a>' % (url, name)


def get_fileuploads(text):
    fileuploads = []

    for match in fileupload_expression.findall(text):
        try:
            fileuploads.append(FileMatch(match))
        except TinyContentFileUpload.DoesNotExist:
            # Just ignore bad slugs
            pass

    return fileuploads


def uploaded_file_filter(content):
    for fileupload_match in get_fileuploads(content):
        content = content.replace(
            fileupload_match.full,
            fileupload_match.tag()
        )

    return content

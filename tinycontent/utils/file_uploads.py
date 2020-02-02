import re
from tinycontent.models import TinyContentFileUpload


fileupload_expression = re.compile(r'(@file:([A-Za-z0-9\-_]+))')


class FileUploadMatch:
    def __init__(self, match):
        self.full = match[0]
        self.file = TinyContentFileUpload.objects.get(
            slug=match[1]
        )


def get_fileuploads(text):
    fileuploads = []

    for match in fileupload_expression.findall(text):
        try:
            fileuploads.append(FileUploadMatch(match))
        except TinyContentFileUpload.DoesNotExist:
            # Just ignore bad slugs
            pass

    return fileuploads

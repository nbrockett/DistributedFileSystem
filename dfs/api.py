from tempfile import TemporaryFile
from tempfile import SpooledTemporaryFile
import requests

FILE_SERVER_ADDR = "http://127.0.0.1:8001/"

## Interface functions:
def open(*args):
    return File(*args)




## Modified Temporary File class
class File(SpooledTemporaryFile):

    def __init__(self, file_path, mode='rtc', cached=False):

        # self.mode = mode
        self.file_path = file_path
        self._mode = mode
        self.is_cached = cached

        SpooledTemporaryFile.__init__(self, 1048576, mode)


    def __exit__(self, exc, value, tb):

        self.close()
        return False

    def close(self):

        SpooledTemporaryFile.flush(self)
        self.post()

    def post(self):

        # if 'a' in self._mode or 'w' in self._mode:
        self.seek(0)
        data = self.read()
        print("data read = ", data)
        post_msg = {'file_name': self.file_path, 'content': data}
        response = requests.post(FILE_SERVER_ADDR, json=post_msg)

        if response.status_code != 200:
            raise Exception("Could not post change of file {0}".format(self.file_path))




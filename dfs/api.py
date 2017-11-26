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

        SpooledTemporaryFile.__init__(self, 100000, mode)

        # reading file
        if 'r' in mode:
            request_arg = {'file_path': file_path}
            response = requests.get(FILE_SERVER_ADDR, request_arg)
            data = response.json()

            # write read file into temp self
            if response.status_code != 204:
                self.write(data['data'])
            else:
                raise Exception("ERROR: Couldn't read file {0}".format(file_path))

    def __exit__(self, exc, value, tb):

        self.close()
        return False

    def read(self, *args):

        # set reading pos to beginning
        self.seek(0)
        print("reading from file")
        return SpooledTemporaryFile.read(self, *args)

    def close(self):

        SpooledTemporaryFile.flush(self)
        if 'a' in self._mode or 'w' in self._mode:
            self.post()

    def post(self):

        # read data
        data = self.read()
        print("data read = ", data)

        # post data to server
        post_msg = {'file_name': self.file_path, 'content': data}
        response = requests.post(FILE_SERVER_ADDR, json=post_msg)

        if response.status_code != 200:
            raise Exception("Could not post change of file {0}".format(self.file_path))




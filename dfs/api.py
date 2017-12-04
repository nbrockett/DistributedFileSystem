from tempfile import SpooledTemporaryFile
import requests
from flask import json
from flask import jsonify
from flask import request
import time
from itertools import count

# ----------------------------------------------------------------------------------------------------------------------
## Setup
def _load_servers_addresses(config_filepath):
    """ return directory server address given in the config file """

    # extract serving_dirs from config file:
    dir_server = None
    with open(config_filepath) as f:
        config_json = json.loads(f.read())
        dir_server = config_json['directory_server']
        lock_server = config_json['locking_server']

    print("DIRECTORY_SERVER form servers.json = ", dir_server)
    print("LOCK_SERVER from server.json = ", lock_server)
    return dir_server, lock_server

DIR_SERVER_ADDR, LOCK_SERVER_ADDR = _load_servers_addresses('servers.json')
# _cached_files = {file_path: SpooledTemporaryFile}
_cached_files = {}
# ----------------------------------------------------------------------------------------------------------------------

## Interface functions:
def open(*args):

    # if cached take given file else create new temp file
    file_path = args[0]
    if file_path in _cached_files:

        fs = _get_file_server(file_path, DIR_SERVER_ADDR)
        request_arg = {'file_path': file_path}
        response = requests.get(fs, request_arg)
        data = response.json()

        if response.status_code != 204:
            return _cached_files[file_path]

    # return new temp file
    return File(*args)

def clear_cache():
    """ clear all caches """
    global _cached_files
    _cached_files = {}

## Modified Temporary File class
class File(SpooledTemporaryFile):

    def __init__(self, file_path, mode='rtc'):

        # self.mode = mode
        self.file_path = file_path
        self._mode = mode
        self.is_cached = False

        # get new client ID from locking server
        try:
            response = requests.get(LOCK_SERVER_ADDR + 'client_id')
            data = response.json()
            self.client_id = data['client_id']
        except requests.exceptions.ConnectionError:
            print("Could not find locking server")
            self.client_id = 0

        # find correct server which hosts file in file_path
        self.server = _get_file_server(file_path, DIR_SERVER_ADDR)

        SpooledTemporaryFile.__init__(self, 100000, mode)

        # poll lock server
        self.poll_lock_server()


        # reading file
        if 'r' in mode:
            request_arg = {'file_path': file_path}
            # print("getting from server ", self.server)
            # print("the file ", file_path)
            response = requests.get(self.server, request_arg)
            # print("repsonse = ", response)
            data = response.json()

            # write read file into temp self
            if response.status_code != 204:
                self.write(data['data'])
            else:
                raise Exception("ERROR: Couldn't read file {0}".format(file_path))

        # if writing to file lock it
        if 'w' in mode or 'a' in mode:
            post_msg = {'file_path': file_path, 'do_lock': True, 'client_id': self.client_id}
            response = requests.post(LOCK_SERVER_ADDR, json=post_msg)

            if response.status_code != 200:
                raise Exception("Could not lock requested file {0}".format(file_path))

    def poll_lock_server(self):
        """ poll lock server until file become unlocked """

        is_locked = True
        while(is_locked):

            request_arg = {'file_path': self.file_path, 'client_id': self.client_id}
            response = requests.get(LOCK_SERVER_ADDR, request_arg)
            data = response.json()
            if data['is_locked']:
                print("File {0} is locked. Polling again".format(self.file_path))
                is_locked = True
                time.sleep(2)
            else:
                is_locked = False

        return

    def read(self, *args):

        # set reading pos to beginning
        self.seek(0)
        print("reading from file")
        return SpooledTemporaryFile.read(self, *args)

    def close(self, cached=False):

        SpooledTemporaryFile.flush(self)

        # unlock file
        if 'a' in self._mode or 'w' in self._mode:
            self.post()

            # unlock file
            post_msg = {'file_path': self.file_path, 'do_lock': False, 'client_id': self.client_id}
            response = requests.post(LOCK_SERVER_ADDR, json=post_msg)

            if response.status_code != 200:
                print("BAD2")

        if cached is True:
            _cached_files[self.file_path] = self

    def post(self):
        """ push temp file to file server"""

        # read data
        data = self.read()
        print("data read = ", data)

        # post data to server
        post_msg = {'file_name': self.file_path, 'content': data}
        response = requests.post(self.server, json=post_msg)

        if response.status_code != 200:
            raise Exception("Could not post change of file {0}".format(self.file_path))



def _get_file_server(file_path, dir_server_addr):
    """ get file server address which hosts the given filepath """

    request_arg = {'file_path': file_path}
    response = requests.get(dir_server_addr, request_arg)
    data = response.json()
    return data['server']


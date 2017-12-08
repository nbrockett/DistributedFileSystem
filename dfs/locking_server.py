import socket
import select
import argparse
from flask import Flask, url_for

from flask import request
from flask import Response
from flask import json
from flask import jsonify

app = Flask(__name__)

from itertools import count

@app.route('/client_id', methods=['GET'])
def get_new_client_id():
    """
    request  : {}

    response : { 'client_id': int }
    """

    data = {'client_id': next(locking_server.client_counter)}
    resp = jsonify(data)
    resp.status_code = 200

    return resp


@app.route('/', methods=['GET'])
def get_lock_status():
    """
    request  : { 'file_path': str
                 'client_id': int}

    response : { 'is_locked': bool }
    """

    file_path = request.args.get('file_path')
    client_id = request.args.get('client_id')

    # get lock status
    is_locked = locking_server.is_locked(file_path, client_id)
    print("Is {0} locked for {2}? {1}".format(file_path, is_locked, client_id))
    data = {'is_locked': is_locked}

    resp = jsonify(data)
    resp.status_code = 200

    return resp

@app.route('/', methods=['POST'])
def post_lock_file():
    """
    request  : { 'file_path': str
                 'do_lcok': bool
                 'client_id': int}

    response : {'lock_status': bool}
    """

    if request.headers['Content-Type'] == 'application/json':

        data = request.json

        file_path = data['file_path']
        do_lock = data['do_lock']
        client_id = data['client_id']


        print("client id = ", client_id)

        if do_lock:
            print("received file path to lock = ", file_path)
            status = locking_server.lock_file(file_path, client_id)
            print("file {0} currently locked for client {1}".format(file_path, client_id))
        else:
            print("received file path to unlock = ", file_path)
            status = locking_server.unlock_file(file_path, client_id)
            print("file {0} currently unlocked from client {1}".format(file_path, client_id))

        print(locking_server.locked_files)

        data_resp = {'lock_status': status}
        resp = jsonify(data_resp)
        resp.status_code = 200

        return resp

    else:
        raise NotImplementedError

class LockingServer:

    def __init__(self, host, port):

        self.host_addr = "http://{0}:{1}/".format(FLAGS.host, FLAGS.port)
        self.host = host
        self.port = port

        # locking server keeps track of client ids in system (everytime a file is opened a new client id is given)
        self.client_counter = count()

        # self.locked_files = {file_path: [list of client ids]}
        self.locked_files = {}

    def lock_file(self, file_path, client_id):
        """ lock file if client_id is first to access. """

        if file_path not in self.locked_files:
            self.locked_files[file_path] = [client_id]
            return True
        elif client_id not in self.locked_files[file_path]:  # if not clients in queue append client to queue
            self.locked_files[file_path].append(client_id)
            return True
        else:  # already locked this file for this client
            return False

    def unlock_file(self, file_path, client_id):
        """ unlock file if clien_id is currently accessing file"""

        if file_path not in self.locked_files:
            raise Exception("Can't unlock file which isn't locked!")
        elif self.locked_files[file_path] != [] and client_id == self.locked_files[file_path][0]:  # if client_id is first in list unlock
            del self.locked_files[file_path][0]
            return True
        else:  # already unlocked this file for this client
            return True

    def is_locked(self, file_path, client_id):
        """ return true if file is currently locked for client_id """

        for fp, val in self.locked_files.items():
            if fp == file_path and self.locked_files[fp] != []:
                if self.locked_files[fp][0] == client_id:
                    return False
                else:
                    return True
        # print("end of line in locked")
        return False

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--host',
        type=str,
        default='127.0.0.1',
        help='host ip of server.'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8004,
        help='port of server.'
    )

    FLAGS, unparsed = parser.parse_known_args()

    # setup locking server
    locking_server = LockingServer(FLAGS.host, FLAGS.port)

    # run application with set flags
    app.run(host=FLAGS.host, port=FLAGS.port)

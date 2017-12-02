import socket
import select
import argparse
from flask import Flask, url_for

from flask import request
from flask import Response
from flask import json
from flask import jsonify
import requests
import datetime
# import Queue

import os
import shutil

app = Flask(__name__)


# SERVING_DIRS = ["/etc", "/src"]

#
# # Adding logging functionality
# import logging
# file_handler = logging.FileHandler('fs.log')
# app.logger.addHandler(file_handler)
# app.logger.setLevel(logging.INFO)


@app.route('/', methods=['GET'])
def get():

    # # example for logging
    # app.logger.info('informing')
    # app.logger.warning('warning')
    # app.logger.error('error')

    print("GET CALLED!")
    file_path = request.args.get('file_path')
    client_id = request.args.get('client_id')


    # get lock status
    is_locked = locking_server.is_locked(file_path, client_id)
    print("Is locked in GET = ", is_locked)
    print("current locked files = ", locking_server.locked_files)
    data = {'is_locked': is_locked}

    resp = jsonify(data)
    resp.status_code = 200

    return resp

@app.route('/', methods=['POST'])
def post():

    print("POST CALLED!")
    if request.headers['Content-Type'] == 'application/json':

        data = request.json

        file_path = data['file_path']
        do_lock = data['do_lock']
        client_id = data['client_id']

        print("received file path to lock = ", file_path)
        print("client id = ", client_id)

        if do_lock:
            status = locking_server.lock_file(file_path, client_id)
        else:
            status = locking_server.unlock_file(file_path, client_id)

        is_locked = locking_server.is_locked(file_path, client_id)

        print("file_path {0} has been set to locked = {1}, status = {2}".format(file_path, do_lock,status))
        print("Is {0} locked? {1}".format(file_path, is_locked))
        print(locking_server.locked_files)


        return "file_path {0} has been set to locked = {1}, status = {2}".format(file_path, do_lock,status)

    else:
        raise NotImplementedError

class LockingServer:

    def __init__(self, host, port):

        self.host_addr = "http://{0}:{1}/".format(FLAGS.host, FLAGS.port)
        self.host = host
        self.port = port
        # self.root_dir = root_dir
        # self.serving_dir = serving_dir
        # self.dir_server = dir_server
        #
        # # reset file server
        # self.reset()
        #
        # # update directory server
        # self.update_dir_server()

        #{file_path: [is_locked, datetime, queue]}
        self.locked_files = {}

        # self.client_queue = Queue.Queue()


    def lock_file(self, file_path, client_id):
        """ """

        # if not self.is_locked(file_path):
        #     # time = datetime.datetime.now()
        #     if file_path not in self.locked_files:
        #         self.locked_files[file_path] = [True, [client_id]]
        #     self.locked_files[file_path][0] = True
        #     self.locked_files[file_path][1].append(client_id)

        if file_path not in self.locked_files:
            self.locked_files[file_path] = [client_id]
            return True
        elif client_id not in self.locked_files[file_path]:  # if not clients in queue append client to queue
            self.locked_files[file_path].append(client_id)
            return True
        else: # already locked this file for this client
            return False

    def unlock_file(self, file_path, client_id):
        """ """

        # if self.is_locked(file_path):
        #     # time = datetime.datetime.now()
        #     self.locked_files[file_path][0] = False

        if file_path not in self.locked_files:
            raise Exception("Can't unlock file which isn't locked!")
        elif self.locked_files[file_path] != [] and client_id == self.locked_files[file_path][0]:  # if client_id is first in list unlock
            del self.locked_files[file_path][0]
            return True
        else:  # already unlocked this file for this client
            return True

    def is_locked(self, file_path, client_id):
        """ """

        for fp, val in self.locked_files.items():
            if fp == file_path and self.locked_files[fp] != []:
                if self.locked_files[fp][0] == client_id:
                    return False
                else:
                    return True
        print("end of line in locked")
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

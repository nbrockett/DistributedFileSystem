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

    # get lock status
    is_locked = locking_server.is_locked(file_path)
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

        print("received file path to lock = ", file_path)

        if do_lock:
            locking_server.lock_file(file_path)
        else:
            locking_server.unlock_file(file_path)

        print("file_path {0} has been set to locked = {1}".format(file_path, do_lock))
        return "file_path {0} has been set to locked = {1}".format(file_path, do_lock)

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

        #{file_path: [is_locked, datetime]}
        self.locked_files = {}


    def lock_file(self, file_path):
        """ """

        if not self.is_locked(file_path):
            time = datetime.datetime.now()
            self.locked_files[file_path] = [True, time]

    def unlock_file(self, file_path):
        """ """

        if self.is_locked(file_path):
            time = datetime.datetime.now()
            self.locked_files[file_path] = [False, time]


    def is_locked(self, file_path):
        """ """

        for fp, val in self.locked_files.items():

            # if file_path is locked return False
            if fp == file_path and val[0] is True:
                return True
            elif fp == file_path and val[0] is False:
                return False
        #

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

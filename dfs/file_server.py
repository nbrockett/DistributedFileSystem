import socket
import select
import argparse
from flask import Flask, url_for

from flask import request
from flask import Response
from flask import json
from flask import jsonify
import requests
import time
import random
import string

import os
import shutil

app = Flask(__name__)

@app.route('/last_modified', methods=['GET'])
def get_last_modified():
    """
    request  : { 'file_path': str}

    response : { 'last_modified': time obj }
    """

    file_path = request.args.get('file_path')
    data = {'last_modified': file_server.get_time_stamp(file_path)}
    resp = jsonify(data)
    resp.status_code = 200

    return resp


@app.route('/', methods=['GET'])
def get_file():
    """
    request  : { 'file_path': str}

    response : { 'data': TextIOWrapper }
    """

    print("GET CALLED!")
    file_path = request.args.get('file_path')

    f = file_server.open_file(file_path)
    if f is None:
        data = {'data': None}
        return jsonify(data)
    else:
        data = {'data': f.read()}

    resp = jsonify(data)
    resp.status_code = 200
    resp.headers['last_modified'] = file_server.get_time_stamp(file_path)
    return resp

@app.route('/', methods=['POST'])
def post_file():
    """
    request  : { 'file_path': str,
                 'content': str }

    response : { 'success': bool }
    """

    data = request.json

    file_path = data['file_path']
    file_content = data['content']

    file_server.create_file(file_path, file_content)

    print("File {0} written to file server".format(file_path))

    data_resp = {'success': True}
    resp = jsonify(data_resp)
    resp.status_code = 200
    resp.headers['last_modified'] = file_server.get_time_stamp(file_path)

    print("DATE IN RESPONSE = ", resp.headers['last_modified'])

    return resp


class FileServer:

    def __init__(self, root_dir, host, port, serving_dir, dir_server):

        self.host_addr = "http://{0}:{1}/".format(FLAGS.host, FLAGS.port)
        self.host = host
        self.port = port
        self.root_dir = root_dir
        self.serving_dir = serving_dir
        self.dir_server = dir_server

        # reset file server
        self.reset()

        # {file_path: internal_file_path}
        self.fpath_to_fpathi = {}

        # update directory server
        self.update_dir_server()

    def create_file(self, file_path, file_content):
        """ create file with internal name"""

        if file_path not in self.fpath_to_fpathi:
            fname_internal = self.generate_name()
            file_path2 = os.path.join(self.root_dir, fname_internal)
        else:  # file already generated
            file_path2 = self.fpath_to_fpathi[file_path]
        f = open(file_path2, 'w')
        f.write(str(file_content))

        # add to internal map
        self.fpath_to_fpathi[file_path] = file_path2

    def open_file(self, file_path):

        try:
            fpath = self.fpath_to_fpathi[file_path]
            return open(fpath)
        except KeyError:
            return None

    def generate_name(self):
        """ generate internal name only the fileserver knows"""

        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))

    def get_time_stamp(self, file_path):
        """ get time stamp of last modification """

        fpath = self.fpath_to_fpathi[file_path]
        return time.ctime(os.path.getmtime(fpath))

    def reset(self):
        """ reset root folder directory"""

        # if root doesnt exist create
        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)

    def update_dir_server(self):
        """ update directory server with new server/directories """

        # post dirs to directory server
        post_msg = {'server': self.host_addr, 'dirs': self.serving_dir}
        response = requests.post(self.dir_server, json=post_msg)

        if response.status_code != 200:
            raise Exception("Unable to update directory server at {0}".format(self.dir_server))

        print("updated directory server")

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
        default=8001,
        help='port of server.'
    )

    parser.add_argument(
        '--config',
        type=str,
        default='fs1.json',
        help='config file for file server'
    )

    FLAGS, unparsed = parser.parse_known_args()

    # extract serving_dirs from config file:
    config_filepath = FLAGS.config
    serving_dirs = ['/']
    dir_server = None
    with open(config_filepath) as f:
        config_json = json.loads(f.read())
        serving_dirs = config_json['serving_dirs']
        dir_server = config_json['directory_server']
        files_root = config_json['files_root']

    print("serving dirs = ", serving_dirs)
    # setup file server
    file_server = FileServer(files_root, FLAGS.host, FLAGS.port, serving_dirs, dir_server)

    # run application with set flags
    app.run(host=FLAGS.host, port=FLAGS.port)

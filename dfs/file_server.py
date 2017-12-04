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
    f_path = file_server.root_dir + file_path
    data = {'last_modified': time.ctime(os.path.getmtime(f_path))}
    resp = jsonify(data)
    resp.status_code = 200


    return resp


@app.route('/', methods=['GET'])
def get():
    """
    request  : { 'file_path': str}

    response : { 'data': TextIOWrapper }
    """

    print("GET CALLED!")
    file_path = request.args.get('file_path')

    if file_path == None:
        # return list of all entries in root_dir of file server
        files = os.listdir(file_server.root_dir)
        data = {
            'files': files,
        }
    else:
        f_path = file_server.root_dir + file_path
        print("getting file ", f_path)
        f = open(f_path)
        print(type(f))
        data = {'data': f.read()}

    # resp2 = Response(data)
    # f_path = file_server.root_dir + file_path
    # resp2.headers['last_modified'] = os.path.getmtime(f_path)
    #
    # return resp2

    resp = jsonify(data)
    resp.status_code = 200
    f_path = file_server.root_dir + file_path
    resp.headers['last_modified'] = time.ctime(os.path.getmtime(f_path))
    return resp

@app.route('/', methods=['POST'])
def post():
    """
    request  : { 'file_name': str,
                 'content': str }

    response : { 'success': bool }
    """

    print("POST CALLED")

    if request.headers['Content-Type'] == 'application/json':

        data = request.json

        file_name = data['file_name']
        file_content = data['content']

        file_path = file_server.root_dir + file_name
        f = open(file_path, 'w')
        f.write(str(file_content))

        print("File {0} written to file server".format(file_path))

        data_resp = {'success': True}
        resp = jsonify(data_resp)
        resp.status_code = 200
        resp.headers['last_modified'] = time.ctime(os.path.getmtime(file_path))

        print("DATE IN RESPONSE = ", resp.headers['last_modified'])

        return resp

    else:
        raise NotImplementedError

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

        # update directory server
        self.update_dir_server()

    def reset(self):
        """ reset root folder directory"""

        # if root doesnt exist create
        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir)

        for serving_dir in self.serving_dir:
            # joined_serving_dir = os.path.join(self.root_dir, serving_dir)

            joined_serving_dir = self.root_dir + serving_dir
            if os.path.exists(joined_serving_dir):
                shutil.rmtree(joined_serving_dir)
                print("making dir: ", joined_serving_dir)
                os.makedirs(joined_serving_dir)
            else:
                print("making dir: ", joined_serving_dir)
                os.makedirs(joined_serving_dir)

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

import socket
import select
import argparse
from flask import Flask, url_for

from flask import request
from flask import Response
from flask import json
from flask import jsonify
import requests

import os
import shutil

app = Flask(__name__)

# TODO: move this to conifg file and load at startup
FILE_DIR_ROOT = "./files_root"
SERVING_DIRS = ["/etc", "/src"]

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

    file_path = request.args.get('file_path')

    if file_path == None:
        # return list of all entries in root_dir of file server
        files = os.listdir(file_server.root_dir)
        data = {
            'files': files,
        }
    else:
        f = open(os.path.join(file_server.root_dir, file_path))
        data = {'data': f.read()}

    resp = jsonify(data)
    resp.status_code = 200

    return resp

@app.route('/', methods=['POST'])
def post():

    # if request.headers['Content-Type'] == 'text/plain':
    #     return "Text Message: " + request.data

    if request.headers['Content-Type'] == 'application/json':

        data = request.json

        file_name = data['file_name']
        file_content = data['content']

        print("received file name = ", file_name)
        print("received content = ", file_content)

        # file_path = os.path.join(file_server.root_dir, file_name)
        # file_path = file_server.root_dir + '/' + file_name
        # file_path = os.path.join(os.getcwd(), file_server.root_dir[2:], file_name)
        # print("file path = ", file_path)
        # print("file path = ", os.path.join(os.getcwd(), file_server.root_dir[2:], file_name))

        file_path = file_server.root_dir + file_name
        f = open(file_path, 'w')
        f.write(str(file_content))


        print("File {0} written to file server".format(file_path))
        return "File {0} written to file server".format(file_path)

    else:
        raise NotImplementedError

class FileServer:

    def __init__(self, root_dir, host, port):

        self.host_addr = "http://{0}:{1}/".format(FLAGS.host, FLAGS.port)
        self.host = host
        self.port = port
        self.root_dir = root_dir
        self.serving_dir = SERVING_DIRS

        # reset file server
        self.reset()

        # update directory server
        self.update_dir_server()

    def reset(self):
        """ reset root folder directory"""

        # if path exists remove directory. Create new root dir
        if os.path.exists(self.root_dir):
            shutil.rmtree(self.root_dir)
            os.makedirs(self.root_dir)
        else:
            os.makedirs(self.root_dir)

        for serving_dir in self.serving_dir:
            # joined_serving_dir = os.path.join(self.root_dir, serving_dir)

            joined_serving_dir = self.root_dir + serving_dir
            print("making dir: ", joined_serving_dir)
            os.makedirs(joined_serving_dir)

    def update_dir_server(self):
        """ update directory server with new server/directories """

        # post dirs to directory server
        post_msg = {'server': self.host_addr, 'dirs': self.serving_dir}
        response = requests.post("http://127.0.0.1:8002/", json=post_msg)

        if response.status_code != 200:
            raise Exception("Unable to update directory server at {0}".format("http://127.0.0.1:8002/"))

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

    FLAGS, unparsed = parser.parse_known_args()

    # setup file server
    file_server = FileServer(FILE_DIR_ROOT, FLAGS.host, FLAGS.port)

    # run application with set flags
    app.run(host=FLAGS.host, port=FLAGS.port)

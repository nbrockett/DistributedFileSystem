import socket
import select
import argparse
from flask import Flask, url_for

from flask import request
from flask import Response
from flask import json
from flask import jsonify

import os
import shutil

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get():

    # # example for logging
    # app.logger.info('informing')
    # app.logger.warning('warning')
    # app.logger.error('error')
    #
    # file_path = request.args.get('file_path')
    #
    # if file_path == None:
    #     # return list of all entries in root_dir of file server
    #     files = os.listdir(file_server.root_dir)
    #     data = {
    #         'files': files,
    #     }
    # else:
    #     f = open(os.path.join(file_server.root_dir, file_path))
    #     data = {'data': f.read()}
    #
    # resp = jsonify(data)
    # resp.status_code = 200
    #
    # return resp

@app.route('/', methods=['POST'])
def post():

    # if request.headers['Content-Type'] == 'text/plain':
    #     return "Text Message: " + request.data

    if request.headers['Content-Type'] == 'application/json':

        data = request.json

        server = data['server']
        directories = data['dirs']

        directory_server.update(server, directories)
        return "Directory Server updated with server {0}".format(server)
    else:
        raise NotImplementedError



class DirectoryServer:

    def __init__(self):

        #{server: [file directories]}
        self.server_files_dic = {}


    def update(self, server, dir_list):

        self.server_files_dic[server] = dir_list
        print("updated, new server-files state: ", self.server_files_dic)

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
        default=8002,
        help='port of server.'
    )

    FLAGS, unparsed = parser.parse_known_args()

    # create directory server
    directory_server = DirectoryServer()

    # run application with set flags
    app.run(host=FLAGS.host, port=FLAGS.port)

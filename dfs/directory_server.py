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
def get_fs():
    """
    request file server address which is responsible for file_path

    request  : { 'file_path': str}

    response : { 'server': str }
    """


    file_path = request.args.get('file_path')
    dir_path = str(os.path.dirname(file_path))

    print("dir_path = ", dir_path)
    print("file_path = ", file_path)

    # find file server serving given dir_path
    for server, dir_list in directory_server.server_files_dic.items():
        if dir_path in dir_list:
            data = {'server': server}
            resp = jsonify(data)
            resp.status_code = 200

            return resp

    # could not find server
    data = {'server': 'NotFound'}
    resp = jsonify(data)
    resp.status_code = 204
    return resp

@app.route('/', methods=['POST'])
def post_fs():
    """
    add file server to the directory server with given directories

    request  : { 'server': str,
                 'dirs', str}

    response : { 'success': bool }
    """

    print("updating directory server...")
    data = request.json

    server = data['server']
    directories = data['dirs']

    # update file server with new entry
    stat = directory_server.update(server, directories)
    if stat is True:
        print("Directory Server updated with server {0} and dirs {1}".format(server, directories))
    data_resp = {'success': stat}
    resp = jsonify(data_resp)
    resp.status_code = 200

    return resp

class DirectoryServer:

    def __init__(self):

        print("initialising directory server")

        #{server: [file directories]}
        self.server_files_dic = {}

    def update(self, server, dir_list):
        """ add file server to servers dictionary"""

        if server not in self.server_files_dic:
            self.server_files_dic[server] = dir_list
            print("updated, new server-files state: ", self.server_files_dic)
            return True
        else:
            print("Could not add file server to directory server. It already has been added")
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
        default=8002,
        help='port of server.'
    )

    FLAGS, unparsed = parser.parse_known_args()

    # create directory server
    directory_server = DirectoryServer()

    # run application with set flags
    app.run(host=FLAGS.host, port=FLAGS.port)

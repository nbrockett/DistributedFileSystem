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
FILE_DIR_ROOT = "./files_root"

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

    # return list of all entries in root_dir of file server
    files = os.listdir(file_server.root_dir)

    data = {
        'files': files,
    }


    # js = json.dumps(data)
    # resp = Response(js, status=200, mimetype='application/json')
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

        file_path = os.path.join(file_server.root_dir, file_name)
        f = open(file_path, 'w')
        f.write(str(file_content))


        print("File {0} written to file server".format(file_path))
        return "File {0} written to file server".format(file_path)

    else:
        raise NotImplementedError

class FileServer:

    def __init__(self, root_dir):

        self.root_dir = root_dir
        self.reset()

    def reset(self):
        """ reset root folder directory"""

        # if path exists remove directory. Create new root dir
        if os.path.exists(self.root_dir):
            shutil.rmtree(self.root_dir)
            os.makedirs(self.root_dir)
        else:
            os.makedirs(self.root_dir)


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
    file_server = FileServer(FILE_DIR_ROOT)

    # run application with set flags
    app.run(host=FLAGS.host, port=FLAGS.port)

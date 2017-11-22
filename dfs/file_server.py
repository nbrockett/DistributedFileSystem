import socket
import select
import argparse
from flask import Flask, url_for

from flask import request
from flask import Response
from flask import json
from flask import jsonify

app = Flask(__name__)




# Adding logging functionality
import logging
file_handler = logging.FileHandler('fs.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)


@app.route('/', methods=['GET'])
def get():

    # example for logging
    app.logger.info('informing')
    app.logger.warning('warning')
    app.logger.error('error')

    data = {
        'hello': 'world',
        'number': 3
    }
    # js = json.dumps(data)
    # resp = Response(js, status=200, mimetype='application/json')
    resp = jsonify(data)
    resp.status_code = 200

    return resp

@app.route('/', methods=['POST'])
def post():

    if request.headers['Content-Type'] == 'text/plain':
        return "Text Message: " + request.data

    elif request.headers['Content-Type'] == 'application/json':
        return "JSON Message: " + json.dumps(request.json)

    elif request.headers['Content-Type'] == 'application/octet-stream':
        f = open('./binary', 'wb')
        f.write(request.data)
        f.close()
        return "Binary message written!"
    else:
        return "415 Unsupported Media Type ;)"


class FileServer:

    def __init__(self):
        self.files = None


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
        default=8000,
        help='port of server.'
    )

    FLAGS, unparsed = parser.parse_known_args()

    # run application with set flags
    app.run(host=FLAGS.host, port=FLAGS.port)

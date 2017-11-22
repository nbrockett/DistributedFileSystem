import socket
import select
import argparse




class DirectoryServer:

    def __init__(self, port=8000, host='localhost'):
        self.host = host
        self.port = port


    def run(self):
        pass


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--host',
        type=str,
        default='localhost',
        help='host ip of server.'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='port of server.'
    )

    FLAGS, unparsed = parser.parse_known_args()

    file_server = DirectoryServer(FLAGS.port, FLAGS.host)
    file_server.run()

import argparse
import logging
from send_file import receive, send

parser = argparse.ArgumentParser(description='Send file in lan')
parser.add_argument('--host', help='Host to send file', type=str)
parser.add_argument('--port', help='Port to send file', type=int)
parser.add_argument('-r', '--receive', help='Mode receive file', action='store_true')
parser.add_argument('-s', '--send', help='Mode send file', action='store_true')
parser.add_argument('-f', '--file', help='Filepath', type=str)

args = parser.parse_args()


def start():
    if args.receive:
        if args.send:
            exit('Only one mode can be selected')

        receive(args.port)

    if args.send:
        if args.receive:
            exit('Only one mode can be selected')
        if not args.host:
            exit('Receive mode need a port')
        if not args.port:
            exit('Insert the port number')

        send(args.file, args.host, args.port)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(message)s')

    logger = logging.getLogger('send_file')
    start()

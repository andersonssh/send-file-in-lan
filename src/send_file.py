import os
import logging
from protocol import get_header
from socketHandlers import ClientHandler

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def send(filepath: str, host: str, port: int):
    """
    Envia o arquivo
    """
    sender = ClientHandler(host, port)

    logger.info('Conectando a %s:%s' % (host, port))
    sender.connect()

    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    logger.info('Enviando arquivo "%s" de %s bytes' % (filename, filesize))

    header = get_header(filename, filesize)

    sender.send_data(header)
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(sender.BUFFER_SIZE)
            if not data:
                break
            sender.send_data(data)

    logger.info('Arquivo enviado!')


if __name__ == '__main__':
    send('ola.txt', 'localhost', 5000)

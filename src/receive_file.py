import logging
from src.protocol import HEADER_OPENING, HEADER_CLOSING
from src.socketHandlers import ServerHandler

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_filename_and_size(data: bytes) -> tuple:
    pos_first_character_of_the_filename = data.find(HEADER_OPENING) \
                                          + len(HEADER_OPENING)
    header = data[pos_first_character_of_the_filename: data.find(HEADER_CLOSING)].decode()
    filename, filesize = header.split(';')

    return filename, filesize


def receive():
    client = ServerHandler()
    client.configure()
    client_socket, addr = client.accept()

    logger.info('Recebendo nome e tamanho do arquivo')
    response = client.receive_data(client_socket, client.BUFFER_SIZE)
    logger.debug('Dados recebidos: %s', response)

    if HEADER_OPENING in response:
        filename, filesize = get_filename_and_size(response)
        logger.info('Arquivo: %s | Tamanho: %s' % (filename, filesize))

        sum_all_characters_from_header = len(filename) + len(filesize) + len(HEADER_OPENING) +\
                                         len(HEADER_CLOSING) + 1  # ";"

        response = response[sum_all_characters_from_header:]

        logger.info('Recebendo dados do arquivo')

        while True:
            with open(filename, 'wb') as f:
                f.write(response)
            response = client.receive_data(client_socket, client.BUFFER_SIZE)
            if not response:
                break

        logger.info('Arquivo recebido!')


if __name__ == '__main__':
    receive()

import logging
from ._protocol import HEADER_OPENING, HEADER_CLOSING
from ._socketHandlers import ServerHandler

logger = logging.getLogger('send_file.receive_file')


def _get_filename_and_size(data: bytes) -> tuple:
    pos_first_character_of_the_filename = data.find(HEADER_OPENING) \
                                          + len(HEADER_OPENING)
    header = data[pos_first_character_of_the_filename: data.find(HEADER_CLOSING)].decode()
    filename, filesize = header.split(';')

    return filename, filesize


def receive(port: int):
    """
    Receive file
    """
    if not port:
        port = 5000

    receiver = ServerHandler(port=port)
    receiver.configure()
    my_ip = receiver.get_my_ip()
    logger.info('Waiting in %s:%s' % (my_ip, port))
    client_socket, addr = receiver.accept()
    logger.info('Connected to %s', addr)

    logger.info('Recebendo nome e tamanho do arquivo')
    response = receiver.receive_data(client_socket, receiver.BUFFER_SIZE)
    logger.debug('Dados recebidos: %s', response)

    if HEADER_OPENING in response:
        filename, filesize = _get_filename_and_size(response)
        logger.info('Arquivo: %s | Tamanho: %s' % (filename, filesize))

        sum_all_characters_from_header = len(filename) + len(filesize) + len(HEADER_OPENING) +\
                                         len(HEADER_CLOSING) + 1  # ";"

        response = response[sum_all_characters_from_header:]

        logger.info('Recebendo dados do arquivo')

        while True:
            with open(filename, 'wb') as f:
                f.write(response)
            response = receiver.receive_data(client_socket, receiver.BUFFER_SIZE)
            if not response:
                break

        logger.info('Arquivo recebido!')

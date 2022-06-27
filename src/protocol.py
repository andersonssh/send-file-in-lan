"""
Protocolos para a comunicação entre o cliente e servidor dessa aplicação.
O envio de dados sempre obedecerá o padrao
--------------------------------------
<#HEADER>FILENAME;SIZE<#/HEADER>DATA
--------------------------------------

exemplo de envio:
--------------------------------------------------------------------------
b'<#HEADER>example.txt;1999<#/HEADER>ARQUIVO DE EXEMPLO'
--------------------------------------------------------------------------
"""
HEADER_OPENING = b'<#HEADER>'
HEADER_CLOSING = b'<#/HEADER>'


def get_header(filename: str, filesize: int):

    return bytes(f'{HEADER_OPENING.decode()}'
                 f'{filename};{filesize}'
                 f'{HEADER_CLOSING.decode()}',
                 encoding='utf-8')


if __name__ == '__main__':
    print(get_header('s', 1))
    print(str(HEADER_OPENING))

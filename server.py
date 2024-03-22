import json
import math
import socket

with open('private.json', 'r') as f:
    key = json.load(f)

with open('public.json', 'r') as f:
    public = json.load(f)

def criptografar(texto: str, e: int, N: int):
    message_bytes = texto.encode()
    message_int = int.from_bytes(message_bytes, byteorder='big')
    encrypted = pow(message_int, e, N)
    return encrypted

def decriptografar(criptografado: int, d: int, N: int):
    decrypted = pow(criptografado, d, N)
    decrypted_bytes = decrypted.to_bytes(math.ceil(decrypted.bit_length() / 8), byteorder='big')
    return decrypted_bytes.decode()

if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('', 5000)
    server_socket.bind(server_address)
    server_socket.listen(1)

    while True:
        print('Aguardando conexão...')
        connection, client_address = server_socket.accept()

        try:
            print(f'Conexão estabelecida com {client_address}')
            key_data = json.dumps(public)
            connection.sendall(key_data.encode())

            while True:
                data = connection.recv(2 ** 20)
                if data:
                    received = int(data.decode('utf8'))
                    message = decriptografar(received, key['key'], key['n'])
                    response = message.upper()
                    crypted_response = criptografar(response, key['key'], key['n'])
                    connection.sendall(str(crypted_response).encode())
                else:
                    break
        finally:
            connection.close()

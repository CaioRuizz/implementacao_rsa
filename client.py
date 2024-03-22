import math
import json
import socket

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
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('127.0.0.1', 5000)
    client_socket.connect(server_address)

    try:
        key_data = client_socket.recv(2 ** 20)
        print(key_data.decode())
        key = json.loads(key_data.decode())

        message = input('Digite o texto que você quer transformar em maiúsculo: ')
        criptografado = criptografar(message, key['key'], key['n'])
        client_socket.sendall(str(criptografado).encode())

        response = int(client_socket.recv(2 ** 20).decode())
        decriptografado = decriptografar(response, key['key'], key['n'])
        print(f'Seu texto em maiúsculo: {decriptografado}')

    finally:
        client_socket.close()

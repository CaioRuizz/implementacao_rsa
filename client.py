import math

import requests


def criptografar(texto: str, e: int, N: int):
    message_bytes = texto.encode()
    message_int = int.from_bytes(message_bytes, byteorder='big')
    encrypted = pow(message_int, e, N)
    return encrypted

def decriptografar(criptografado: int, d: int, N: int):
    decrypted = pow(criptografado, d, N)
    decrypted_bytes = decrypted.to_bytes(math.ceil(decrypted.bit_length() / 8), byteorder='big')
    return decrypted_bytes.decode()

def main():
    key = requests.get('http://127.0.0.1:5000/get_key').json()

    message = input('Digite o texto que você quer transformar em maiúsculo: ')
    criptografado = criptografar(message, key['key'], key['n'])
    response = int(requests.post('http://127.0.0.1:5000', f'{criptografado}').text)
    decriptografado = decriptografar(response, key['key'], key['n'])
    print(f'seu texto em maiúsculo: {decriptografado}')

if __name__ == '__main__':
    main()
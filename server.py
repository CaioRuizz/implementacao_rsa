import json
import math

from flask import Flask, request

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


app = Flask(__name__)


@app.route('/get_key')
def get_key():
    return json.dumps(key)


@app.route('/', methods=['POST'])
def index():
    received = int(request.data.decode('utf8'))
    message = decriptografar(received, key['key'], key['n'])
    response = message.upper()
    crypted_response = criptografar(response, key['key'], key['n'])
    return str(crypted_response)

if __name__ == '__main__':
    app.run(debug=True)
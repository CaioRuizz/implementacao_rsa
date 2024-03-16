import random
import math

frase = 'The information security is of significant importance to ensure the privacy of communications.'

def is_prime(n, k=40):  # number of tests = k
   #n = int.from_bytes(num_bytes, 'big')
   if n <= 1:
       return False
   if n <= 3:
       return True
   if n % 2 == 0:
       return False
   if n % 5 == 0:
       return False
   
   r, d = 0, n - 1
   while d % 2 == 0:
       r += 1
       d //= 2
   for _ in range(k):
       a = random.randrange(2, n - 1)
       x = pow(a, d, n)  # a^d % n
       if x == 1 or x == n - 1:
           continue
       for _ in range(r - 1):
           x = pow(x, 2, n)
           if x == n - 1:
               break
       else:
           return False
   return True

def get_two_prime_numbers() -> list[int]:
    response = []
    while True:
        if len(response) == 2:
            return response
        
        number = random.getrandbits(2048)
        if is_prime(number) and number not in response:
            response.append(number)

def MDC(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a

def coprime(a: int, b: int) -> bool:
    return MDC(a, b) == 1

def criptografar(texto: str, e: int, N: int):
    message_bytes = texto.encode()
    message_int = int.from_bytes(message_bytes, byteorder='big')
    encrypted = pow(message_int, e, N)
    return encrypted

def decriptografar(criptografado: int, d: int, N: int):
    decrypted = pow(criptografado, d, N)
    decrypted_bytes = decrypted.to_bytes(math.ceil(decrypted.bit_length() / 8), byteorder='big')
    return decrypted_bytes.decode()

def extended_euclidean_algorithm(a: int, b: int):
        if a == 0:
            return (b, 0, 1)
        else:
            gcd, x, y = extended_euclidean_algorithm(b % a, a)
            return (gcd, y - (b // a) * x, x)

def find_d(e: int, fiN):
    gcd, x, y = extended_euclidean_algorithm(e, fiN)
    if gcd != 1:
        raise ValueError(f"{e} não tem inverso multiplicativo modulo {fiN}")
    else:
        return x % fiN


def get_rsa():
    while True:
        p, q = get_two_prime_numbers()
        
        N = p * q

        fiN = (p - 1) * (q - 1)

        e = fiN - 1

        if coprime(fiN, e):
            break

    d = find_d(e, fiN)

    return e, d, N

if __name__ == '__main__':
    e, d, N = get_rsa()
    print('Criptografando')
    criptogrado = criptografar(frase, e, N)
    print('Decriptografando')
    decriptogrado = decriptografar(criptogrado, d, N)

    print('Exibindo resultados')

    print(f'{criptogrado=}')
    print(f'{decriptogrado=}')
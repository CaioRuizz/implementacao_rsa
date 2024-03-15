import random

frase = 'The information security is of significant importance to ensure the privacy of communications.'

def is_prime(number: int) ->  bool:
    if number <= 1:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True

def get_two_prime_numbers() -> list[int]:
    response = []
    while True:
        if len(response) == 2:
            return response
        
        number = random.randint(2, 2 ** 8)
        if is_prime(number) and number not in response:
            response.append(number)

def MDC(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a

def coprime(a: int, b: int) -> bool:
    return MDC(a, b) == 1

def criptografar(texto: str, e: int, N: int):
    response = ''
    for char in texto:
        p = ord(char)
        response += chr((p ** e) % N)
    return response

def decriptografar(texto: str, d: int, N: int):
    response = ''
    for char in texto:
        p = ord(char)
        response += chr((p ** d) % N)
    return response


if __name__ == '__main__':
    while True:
        print('Definindo p e q')
        p, q = get_two_prime_numbers()
        
        print('Calculando N')
        N = p * q

        print('Calculando Φ(N)')
        ΦN = (p - 1) * (q - 1)

        print('Calculando e')
        e = ΦN - 1

        print('Validando de Φ(N) e "e" são primos entre si')
        if not coprime(ΦN, e):
            print('Não são primos entre si, tentando novamente')
            continue
        else:
            print('São primos entre si')
            break

    print('Calculando d')
    d = 0
    while  (e * d) % ΦN != 1:
        d += 1

    print('Criptografando')
    criptogrado = criptografar(frase, e, N)
    print('Decriptografando')
    decriptogrado = decriptografar(criptogrado, d, N)

    print('Exibindo resultados')

    print(f'{criptogrado=}')
    print(f'{decriptogrado=}')
import math
import rsa_math


def gen_keys():
    p, q = rsa_math.get_prime(500), rsa_math.get_prime(550)
    n = p * q
    eul = (p - 1) * (q - 1)
    while True:
        e = 65537
        if math.gcd(e, eul) == 1:
            break
        else:
            e -= 1
    d = rsa_math.mod_1(e, eul)
    return {'n': n, 'e': e, 'd': d}


def encrypt(plaintext, e, n):
    return pow(plaintext, e, n)


def decrypt(cyphertext, d, n):
    return pow(cyphertext, d, n)

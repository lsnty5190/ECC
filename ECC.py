'''
Author: your name
Date: 2021-05-27 16:41:11
LastEditTime: 2021-06-01 16:40:03
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \第九次作业\ECC.py
'''
import numpy as np

def exgcd(a, b):

    if b == 0:
        return 1, 0, a
    else:
        x, y, q = exgcd(b, a % b)
        x, y = y, (x - (a // b) * y)
        return x, y, q

def inverse(a, b):
    
    return exgcd(a, b)[0]

def add(P, Q, a, p):
    # slope is positive
    flag = 1

    # claculate k
    if P == Q:
        # iterative P (kP)
        # nume: numerator
        # deno: denominator
        nume = 3 * (P[0] ** 2) + a
        deno = 2 * P[1]

    else:
        # y distance
        nume = Q[1] - P[1]
        # x distance
        deno = Q[0] - P[0]

        if nume * deno < 0:
            # slope is negtive
            flag = -1
            nume = abs(nume)
            deno = abs(deno)

    # reduction
    gcd = exgcd(nume, deno)[2]
    nume = nume // gcd
    deno = deno // gcd

    # compute final slope mod p
    k = flag * nume * inverse(deno, p)
    k %= p

    # compute R = (P + Q)
    R_x = (k ** 2 - P[0] - Q[0]) % p
    R_y = (k * (P[0] - R_x) - P[1]) % p

    return [R_x, R_y]

'''def linear_add(P, k, a, p):
    R = [P[0], P[1]]
    # R = kP
    for i in range(k-1):
        R = add(R, P, a, p)
    return R'''

def linear_add(x, n, a, p):
    """
    quick multiply using "divide and conquer"

    :param n: int
    :param x: ECPoint
    :return: n * x
    """
    
    if n == 1:
        return x
    else:
        if n & 1 == 1:
            mid = linear_add(x, n // 2, a, p)
            return add(x, add(mid, mid, a, p), a, p)
        else:
            mid = linear_add(x, n // 2, a, p)
            return add(mid, mid, a, p)

def minus(P, Q, a, p):
    Q = [Q[0], -1 * Q[1] % p]
    return add(P, Q, a, p)

def rank(G, a, b, p):

    n = 1
    targ = [G[0], (-1 * G[1]) % p]
    tmp = G
    while True:
        n += 1
        P = add(tmp, G, a, p)
        if P == targ:
            return n + 1
        tmp = P

def enc_ECC(a, b, p, G, private_key, Pm, k):

    # verify
    if (4*(a**3)+27*(b**2))%p == 0:
        assert "The Chosen point isn't on elliptic curve!"

    # private key is provided by user A
    # public_key = private_key * G
    public_key = linear_add(G, private_key, a, p)
    print('public key:', public_key)
    # user A gives [Ep(a,b), public_key, G] to user B

    # user B encode the message to Pm and generate a random integer k(k<n)
    k_G = linear_add(G, k, a, p)
    k_public = linear_add(public_key, k, a, p)
    Cm = [k_G, add(Pm, k_public, a, p)]

    return Cm

def dec_ECC(a, p, private_key, Cm):
    
    return minus(Cm[1], linear_add(Cm[0], private_key, a, p), a, p)

def DH(a, b, q, G, na, nb):

    # user A
    Pa = linear_add(G, na, a, q)
    print(Pa)
    # user B
    Pb = linear_add(G, nb, a, q)
    print(Pb)

    Ka = linear_add(Pb, na, a, q)
    Kb = linear_add(Pa, nb, a, q)

    if Ka != Kb:
        assert "Under Attack!"
    else:
        print("Connection Success!")

def test_ECC():
    a = 0
    b = -4
    p = 257
    Pm = [112, 26]
    k = 41
    G = [2, 2]
    private_key = 101
    Cm = enc_ECC(a, b, p, G, private_key, Pm, k)
    print(Cm)
    DePm = dec_ECC(a, p, private_key, Cm)
    print(DePm)

def test_DH():
    q = 0x8542d69e4c044f18e8b92435bf6ff7de457283915c45517d722edb8b08f1dfc3
    a = 0x787968b4fa32c3fd2417842e73bbfeff2f3c848b6831d7e0ec65228b3937e498
    b = 0x63e4c6d3b23b0c849cf84241484bfe48f61d59a5b16ba06e6e12d1da27c5249a
    G = [0x421debd61b62eab6746434ebc3cc315e32220b3badd50bdc4c4e6c147fedd43d, 0x0680512bcbb42c07d47349d2153b70c4e5d7fdfcbfa36ea1a85841b9e46e09a2]
    na = 0x111e32da4d217b865cccb70c847603121eae9bfd95bdf399af626d23c05c742c
    nb = 0x4f593b08c8831a5219c961e1a3406401b20655492e5000b1fb5793241501e931
    '''a = 0
    b = -4
    q = 257
    G = [2, 2]
    na = nb = 101'''
    DH(a, b, q, G, na, nb)

if __name__ == '__main__':
    test_DH()
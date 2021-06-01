'''
Author: your name
Date: 2021-05-28 15:17:05
LastEditTime: 2021-05-28 17:41:53
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \第九次作业\SM2.py
'''
from numpy import lib
from ECC import linear_add
import hashlib
import libnum
import math

def KDF(Z, klen):
    # in sha-512, v = 512
    v = 512

    # initialize a counter
    ct = 0x000001
    Ha = []
    hash = hashlib.sha512()

    for i in range(math.ceil(klen / v)):
        vat = int(hex(Z)[2:].zfill(klen // 4) + hex(ct)[2:].zfill(8), 16)
        hash_pre = libnum.n2s(vat).decode()
        hash.update(hash_pre.encode())
        p = hash.hexdigest()
        Ha.append(bin(int(p, 16))[2:].zfill(512))
        ct += 1

    if klen % v == 0:
        keep = klen - math.floor(klen / v) * v
        Ha_tail = bin(Ha[-1])[2:].zfill(512)[:keep]
        Ha.append(Ha_tail)
    else:
        Ha_tail = Ha[-1]
        Ha.append(Ha_tail)
    
    # print(Ha)
    K = ''.join(Ha)
    
    return K


def enc_SM2(a, p, M, G, Pb):

    while True:
        # k \in [0, n-1]
        k = 0x46889d7648c981d63bce3dca278374d184f8acba0400e4690edb0772e5ea2137

        C1 = linear_add(G, k, a, p)
        print(C1)
        Q = Pb * k

        
        



def test_SM2():
    a = 0xfffffffeffffffffffffffffffffffffffffffff00000000fffffffffffffffc
    p = 0xfffffffeffffffffffffffffffffffffffffffff00000000ffffffffffffffff
    G = [0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7,
         0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0]
    Pb = [0x9a8d4c4599edbc66d35c1fd07d17473c004eed30cdf6afb92ab15f480479a599,
          0x78d82462cc31e2cf5d477b6d872b604fde31d8d25e2d0b60dc78ba87ba3eadd4]
    M = ''

    enc_SM2(a, p, M, G, Pb)
    
def test_KDF():
    M = 'testsm4'.encode().hex()

    K = KDF(int(M, 16), len(M)*4)
    print(hex(int(K, 2)))


if __name__ == '__main__':
    test_SM2()
    

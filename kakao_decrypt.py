from Crypto.Cipher import AES
import hashlib
import base64
from hashlib import pbkdf2_hmac

def genSalt(user_id):
    incept = 'extr.ursra'
    salt = incept + str(user_id)
    salt = salt[0:16].encode()
    return salt

def adjust(a, aOff, b):
    x = (b[len(b) - 1] & 255) + (a[aOff + len(b) - 1] & 255) + 1
    a[aOff + len(b) - 1] = x % 256
    x = x >> 8
    for i in range(len(b)-2, -1, -1):
        x = x + (b[i] & 255) + (a[aOff + i] & 255)
        a[aOff + i] = x % 256
        x = x >> 8   

def deriveKey(password, salt, iterations, dkeySize):
    password = (password + b'\0').decode('ascii').encode('utf-16-be')
    
    hasher = hashlib.sha1()
    v = hasher.block_size
    u = hasher.digest_size

    D = [ 1 ] * v
    S = [ 0 ] * v * int((len(salt) + v - 1) / v)
    for i in range(0, len(S)):
        S[i] = salt[i % len(salt)]
    P = [ 0 ] * v * int((len(password) + v - 1) / v)
    for i in range(0, len(P)):
        P[i] = password[i % len(password)]

    I = S + P

    B = [ 0 ] * v
    c = int((dkeySize + u - 1) / u)

    dKey = [0] * dkeySize
    for i in range(1, c+1):
        hasher = hashlib.sha1()
        hasher.update(bytes(D))
        hasher.update(bytes(I))
        A = hasher.digest()

        for j in range(1, iterations):
            hasher = hashlib.sha1()
            hasher.update(A)
            A = hasher.digest()

        A = list(A)
        for j in range(0, len(B)):
            B[j] = A[j % len(A)]

        for j in range(0, int(len(I)/v)):
            adjust(I, j * v, B)

        start = (i - 1) * u
        if i == c:    
            dKey[start : dkeySize] = A[0 : dkeySize-start]
        else:
            dKey[start : start+len(A)] = A[0 : len(A)]

    return bytes(dKey)

def decrypt(user_id, b64_ciphertext):
    password = b'\x16\x08\x09\x6f\x02\x17\x2b\x08\x21\x21\x0a\x10\x03\x03\x07\x06'
    iv = b'\x0f\x08\x01\x00\x19\x47\x25\xdc\x15\xf5\x17\xe0\xe1\x15\x0c\x35'

    salt = genSalt(user_id)
    key = deriveKey(password, salt, 2, 32)

    Cipher = AES.new(key, AES.MODE_CBC, iv)
    
    ciphertext = base64.b64decode(b64_ciphertext)
    padded = Cipher.decrypt(ciphertext)
    plaintext = padded[:-padded[-1]]
    return plaintext.decode('UTF-8')
    

if __name__ == '__main__':
    content = 'AqxvJzJSZ6PZSR3nX+qDYw=='
    user_id = 126176232

    content = 'jdheji4B4hWnj7RVYCGeQvjjexDSmcErJwlkAlLb0y+AlTkRsYyua+x15pPyha5z2bYtnYZkHX5lTRrzeKXDfLZaWU6IF/cBn9BNsM/TPEQ='


    content = 'jdheji4B4hWnj7RVYCGeQlvnaIZ9fmU4q4dwiqYynyc/dNFNOIyQc61jigEt\
        wDRlXdjpaUgzxHcSP9r9vZkNC39nMeHt7/1yCJju42UcF2DfCBq1EKm+oxdEMuZdOuxR'
    content = 'Xq4AghEzWFP4iZ7XXGMD66GZHhP2YI8rgBITRbCWWnjN+ckjaQetxjn7CEYRYgMvZyBnAaN5JtzqWd+L0RHYIyfZuZRNdCgXARwEfPoPh2O5Tl6k1tFp+tkHy1ixx2sTCd3qyAzxkgCamVllzZi/snBZhpgBWBAZ+oEwv/GVKzvCLuSwfm0V5PNuOCxCwKzW/ALtXvSsqmPoIN5GJ+1U1BEzVSgDtX2N6sD9suv+FFDUadv9uMn1vYTUMuQoWKZMUmZ5kL62nd75dAqIaosZUkUW9ebr1K/LWl9OHYaK9eiILtQ7Do2nlHmbW6gnhMojQ0tjVbMUNf6O5Fch0HtbDTz5rG21sRau78pPB1HuNn5ghQQpq6DqU1nn8+5XppSh+S4GrQAamhqRbe5gnuP27hc2gAhw2dXqzSWJj9VeZPXrXHfOlAWDodEtZbNEOHVcxlpKPqsmtlNMQ6YsNn24RF0i7BWy3EwInJtmVp/Fu8m7DcRkZ5qa9ltANTM/Ollajrfwx7un+oG1uGv5f1k0PJyr50T29EvxGDEcJUt3dE0='

    content = 'r1CaIcaNneOkWg0SPlki/A=='
    user_id = 64081481
    dec = decrypt(user_id, content)
    print(dec)


import hashlib
from Crypto.Cipher import AES
import base64


def purple_dec(userId, enc_msg):
    key = hashlib.sha256(userId.encode()).digest()
    decoded_msg = base64.b64decode(enc_msg)
    iv = bytes(16)
    Cipher = AES.new(key,AES.MODE_CBC,iv)
    dec_msg = Cipher.decrypt(decoded_msg)
    plaintext = dec_msg[:-dec_msg[-1]]

    return plaintext.decode('utf-8')



if __name__ == '__main__':
    userId = '4566B3F4-81A1-42F0-9929-5B53EE5985C6'
    enc_msg = "hLbIbhipR+jyKUjd9+pzcDmBT2pvJgfPlWkJg3z1Lx2q18Q0VDcaDjNyd9S3mXi1s1+e69nuT5zAExZWGj3Z1A=="
    dec_msg = purple_dec(userId, enc_msg)
    print(dec_msg)
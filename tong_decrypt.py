import hashlib
from Crypto.Cipher import AES
import base64

def tong_dec(userId, enc_msg):
    decoded_msg = base64.b64decode(enc_msg)

    concatenate_userId = (userId + "*" + userId).encode()
    s = hashlib.sha256(concatenate_userId).digest()
    ss = base64.b64encode(s)

    key = hashlib.sha256(ss).digest()
    iv = hashlib.md5(ss).digest()

    Cipher = AES.new(key, AES.MODE_CBC, iv)
    dec = Cipher.decrypt(decoded_msg)
    dec_msg = dec[:-1*dec[-1]]

    return dec_msg.decode()

if __name__ == '__main__':

    userId = "1618494296!usr-c6912bc5-ff9a-4c69-825c-91e3bc204e00@tongchat.com"
    enc_msg = "ySuBlRx2s8Ppq741/ffreg=="
    dec_msg = tong_dec(userId, enc_msg)
    print(dec_msg)
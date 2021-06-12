import hashlib
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
import binascii
import os

def wickrDB_key(skdata, password):
    salt=skdata[1:17]
    gcm_nonce = skdata[18:30]
    gcm_tag = skdata[30:46]
    ciphertext = skdata[46:]
    K = scrypt(password, salt, N=131072, r=8, p=1, key_len=32)

    Cipher = AES.new(K, AES.MODE_GCM, nonce=gcm_nonce)
    dec = Cipher.decrypt_and_verify(ciphertext, gcm_tag)
    dbpass = binascii.hexlify(dec[4:37]).decode()

    return dbpass

def wickr_media(mdk, mediaPath):
    f = open(mediaPath, 'rb')
    mediadata = f.read()
    f.close()

    gcm_nonce = mediadata[1:13]    
    cipher = mediadata[29:]
    
    Cipher = AES.new(mdk, AES.MODE_GCM, nonce=gcm_nonce)
    dec = Cipher.decrypt(cipher)

    return dec
    
'''
f=open('C:/MDTool/SM-G955N/20210612-Wickr-001/Wickr/files/sk.wic', 'rb+')
data=f.read()
f.close()
print(data)
password = 'dltndk11@@'

dbpass = wickrDB_key(data, password)
print(dbpass)
'''

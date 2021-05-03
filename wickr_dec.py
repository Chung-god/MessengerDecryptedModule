import hashlib
from Crypto.Cipher import AES
import binascii
import scrypt


"""password = str(input('사용자 비밀번호 입력 : '))
password.encode()"""
password="dltndk11@@".encode()
N=131072 #고정값
r=8 #고정값
p=1 #고정값
dklen=32 #고정값

F = open('C:/Program Files (x86)/Nox/bin/MyWicker/files/sk.wic','rb+')
data = F.read()

#salt 추출
salt = data[1:17]

#gcm 추출
gcm = data[18:30]

#ciphertext 추출
ciphertext = data[46:]

#scrypt함수에 사용자 비밀번호와 초기 파라미터 값으로 aes 암호 키값 생성
K = scrypt.hash(password, salt, N, r, p, dklen)

#aes256_gcm_mode에 scrypt key 값과 gcm nonce 값설정 후 cipher 변수 저장
cipher = AES.new(K, AES.MODE_GCM,gcm)

#cipher 변수에 ciphertext넣고 복호화 시작
i = cipher.decrypt(ciphertext)

#복호화된 데이터베이스 암호 텍스트파일 저장
f=open('wickr_pwd_test1.txt', 'wb+')
f.write(i)
f.close()

#저장된 파일 오픈
f = open('C:/Users/이정호/Desktop/케이쉴드/프로젝트/project/wickr_pwd_test1.txt','rb+')
password = f.read()

dbpass = str(binascii.hexlify(password[4:37]))
print(dbpass)

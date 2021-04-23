from pysqlcipher3 import dbapi2 as sqlcipher
db = sqlcipher.connect('user.db') # db이름
db.execute('pragma key="00ed506ee2684412fb59736ff090a7c6a87324627e420533b468c45139d732cf"') # 암호
cur = db.cursor()
cur.execute("select * from users") # 불러올 table 이름
row = cur.fetchone()

print("고유 번호(idx) : ", row[1])
print("토큰 : ", row[3])
print("이메일 : ", row[4])
print("이름: ", row[5])
print("상태 메시지: ", row[6])
print("핸드폰 번호: ", row[7])
print("친구 목록(idx) : ", row[12])
print("친한친구 목록 : ", row[13])

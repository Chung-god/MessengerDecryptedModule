from pysqlcipher3 import dbapi2 as sqlcipher
db = sqlcipher.connect('user.db')
db.execute('pragma key="00ed506ee2684412fb59736ff090a7c6a87324627e420533b468c45139d732cf"')
cur = db.cursor()

cur.execute("select * from sqlite_sequence")
row = cur.fetchone()
num_rows = row[1] - 1

cur.execute("select * from users")
for x in range(0, num_rows):
    row = cur.fetchone()
    #print(row)
    print("고유 번호(idx) : ", row[1])
    print("토큰 : ", row[3])
    print("이메일 : ", row[4])
    print("이름: ", row[5])
    print("상태 메시지: ", row[6])
    print("핸드폰 번호: ", row[7])
    print("친구 목록(idx) : ", row[12])
    print("친한친구 목록 : ", row[13])
    print("새로 추가한 친구 목록 : ", row[14])
    print("차단한 친구 목록 : ", row[15])
    print("친구 요청 목록 : ", row[16])
    print("프로필 바탕화면 사진(json) : ", row[18])
    print("친구 신청시 표시되는 문구 : ", row[31])
    print("--------------------------")

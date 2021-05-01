from pysqlcipher3 import dbapi2 as sqlcipher
from lysn_key import userDB_key, talkDB_key

# lysn user.db 내용 추출 
def lysn_userDB(dbfile, android_id):
    userkey = userDB_key(android_id) # user.db key 구하기

    # db 열기
    db = sqlcipher.connect(dbfile)
    db.execute('pragma key="'+userkey+'"')
    cur = db.cursor()

    # 추출할 내용 지정
    colname = {'username':'이름', 'useridx':'고유 번호(idx)', 'userId':'이메일', 'phoneNo':'핸드폰 번호', 'inviteName':'친구 신청시 표시되는 문구'}
    rowlist = export(cur, 'users', colname) # user.db에 users 테이블 내용 추출
    return colname.values(), rowlist

# lysn talk.db 내용 추출
def lysn_talkDB(dbfile, android_id):
    # user.db 먼저 열어서 useridx 값 받아오기
    udbfile=dbfile.replace('talk.db', 'user.db')
    ulist = lysn_userDB(udbfile, android_id)[1]
    useridx = ulist[0][1]
    
    # db 열기
    db = sqlcipher.connect(dbfile)
    talkkey = talkDB_key(useridx)
    db.execute('pragma key="'+talkkey+'"')
    cur = db.cursor()

    # 추출할 내용 지정
    colname = {'time':'시간', 'sender':'보낸사람', 'type':'타입', 'roomidx':'채팅방 번호', 'text':'메시지'}
    rowlist = export(cur, 'chats', colname) # talk.db에 chats 테이블 내용 추출
    
    # 이름과 고유번호 가져오기
    for i in range(len(rowlist)):
        for urow in ulist:
            if rowlist[i][1] == urow[1]:
                rowlist[i][1] = urow[0]
    
    return colname.values(), rowlist

# 내용 추출하기
def export(cur, table, colname):
    cur.execute('pragma table_info('+table+')')
    rows = cur.fetchall()
    col_defs = { row[1]: row[0] for row in rows }

    cur.execute("SELECT * FROM "+table)
    rows = cur.fetchall()

    # 추출할 내용에 따라 각 행 내용을 리스트로 저장하기
    rowlist = []
    for row in rows:
        d_row = [row[col_defs[i]] for i in colname.keys()]
        rowlist.append(d_row)
    return rowlist

if __name__ == '__main__':
    '''
    dbfile = "com.everysing.lysn/databases/user.db"
    colname, rowlist = lysn_userDB(dbfile)
    
    print(colname)
    for row in rowlist:
        print(row)
    '''
    dbfile = "com.everysing.lysn/databases/talk.db"
    colname, rowlist = lysn_talkDB(dbfile)
    print(colname)
    for row in rowlist:
        print(row)
from pysqlcipher3 import dbapi2 as sqlcipher
from lysn_key import userDB_key, talkDB_key

# lysn user.db 내용 추출 
def lysn_userDB(dbfile, android_id):
    app = 'lysn'
    userkey = userDB_key(android_id) # user.db key 구하기

    # db 열기
    db = sqlcipher.connect(dbfile)
    db.execute('pragma key="'+userkey+'"')
    cur = db.cursor()

    # 추출할 내용 지정
    colname = {'username':'이름', 'useridx':'고유 번호(idx)', 'userId':'이메일', 'phoneNo':'핸드폰 번호', 'inviteName':'친구 신청시 표시되는 문구'}
    rowlist = export(app, cur, 'users', colname) # user.db에 users 테이블 내용 추출
    return colname.values(), rowlist

# lysn talk.db 내용 추출
def lysn_talkDB(dbfile, android_id):
    app = 'lysn'

    # user.db 먼저 열어서 useridx 값 받아오기
    udbfile=dbfile.replace('talk.db', 'user.db')
    ulist = lysn_userDB(udbfile, android_id)[1]
    useridx = ulist[0][1]
    
    # db 열기
    db = sqlcipher.connect(dbfile)
    talkkey = talkDB_key(useridx)
    db.execute('pragma key="'+talkkey+'"')
    cur = db.cursor()

    # chats 테이블 추출할 내용 지정
    chatsColname = {'time':'시간', 'sender':'보낸사람', 'type':'타입', 'roomidx':'채팅방 번호', 'text':'메시지'}
    chatsRowlist = export(app, cur, 'chats', chatsColname, ulist) # talk.db에 chats 테이블 내용 추출
    
    # rooms 테이블 추출할 내용 지정
    roomsColname = {'roomidx':'채팅방 번호', 'name':'채팅방 인원', 'lastChatTime':'시간', 'lastChatSender':'마지막 보낸사람', 'lastChatType':'타입', 'lastChatText':'마지막 보낸 메시지'}
    roomsRowlist = export(app, cur, 'rooms', roomsColname, ulist) # talk.db에 rooms 테이블 내용 추출
    
    return chatsColname.values(), chatsRowlist, roomsColname.values(), roomsRowlist


def lysnConversation(row, colname, col_defs, compare):
    d_row=[]
    for en, kr in colname.items():
        value = row[col_defs[en]]
        # 시간 변환
        if kr == '시간' and value != None:
            value = str(str(value[0:2])+"년 " + str(value[2:4])+"월 " 
            + str(value[4:6])+"일 " + str(value[6:8])+"시 " + str(value[8:10])+"분 " + str(value[10:12])+"초")
        # 이름 변환
        elif (kr == '보낸사람' or kr == '마지막 보낸사람') and compare != None:
            for ulist in compare:
                if value == ulist[1]:
                    value = ulist[0]
        # 채팅방 인원 이름 변환
        elif kr == '채팅방 인원':
            names = value.split('.')
            
            for i in range(len(names)):
                for ulist in compare:
                    if names[i] == ulist[1]:
                        names[i] = ulist[0]
                
            value = ', '.join(names)    

        d_row.append(value)

    return d_row
    
# 내용 추출하기
def export(app, cur, table, colname, compare = None):
    cur.execute('pragma table_info('+table+')')
    rows = cur.fetchall()
    col_defs = { row[1]: row[0] for row in rows }

    cur.execute("SELECT * FROM "+table)
    rows = cur.fetchall()

    # 추출할 내용에 따라 각 행 내용을 리스트로 저장하기
    if app == 'lysn':
        rowlist = [lysnConversation(row,colname,col_defs,compare) for row in rows]
    return rowlist


if __name__ == '__main__':
    '''
    dbfile = "com.everysing.lysn/databases/user.db"
    colname, rowlist = lysn_userDB(dbfile)
    
    print(colname)
    for row in rowlist:
        print(row)
    '''
    dbfile = "lysn/com.everysing.lysn/databases/talk.db"
    android_id = '4f77d977f3f1c488'

    colname, rowlist, colname2, rowlist2 = lysn_talkDB(dbfile, android_id)
    
    print(colname2)
    for row in rowlist2:
        print(row)
    
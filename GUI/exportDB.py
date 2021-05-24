from pysqlcipher3 import dbapi2 as sqlcipher
from Crypto.Cipher import AES
import hashlib
import base64
import os
import datetime

from lysn_key import userDB_key, talkDB_key
from tong_decrypt import tong_dec
from wickr_decrypt import wickrDB_key, wickr_media

# lysn user.db 내용 추출 
def lysn_userDB(path, android_id):
    app = 'lysn'
    userkey = userDB_key(android_id) # user.db key 구하기

    # db 열기
    dbfile = path + 'databases/user.db'
    db = sqlcipher.connect(dbfile)
    db.execute('pragma key="'+userkey+'"')
    db.execute('PRAGMA cipher_compatibility = 3')
    cur = db.cursor()

    # 테이블 추출할 내용 지정
    # users
    userColname = {'username':'이름', 'useridx':'고유 번호(idx)', 'userId':'이메일', 'phoneNo':'핸드폰 번호', 'inviteName':'친구 신청시 표시되는 문구'}
    userRowlist = export(app, cur, 'users', userColname) # user.db에 users 테이블 내용 추출
    
    # sqlite_sequence
    seqColname = {'name':'테이블 이름', 'seq':'레코드 개수'}
    seqRowlist = export(app, cur, 'sqlite_sequence', seqColname) # user.db에 sqlite_sequence 테이블 내용 추출
    
    colname = [userColname.values(), seqColname.values()]
    rowlist = [userRowlist, seqRowlist]

    return colname, rowlist

# lysn talk.db 내용 추출
def lysn_talkDB(path, android_id, rowlist):
    app = 'lysn'
    dbfile = path + 'databases/talk.db'
    
    # user.db 먼저 열어서 useridx 값 받아오기
    ulist = rowlist[0]
    useridx = ulist[0][1]
    
    # db 열기
    db = sqlcipher.connect(dbfile)
    talkkey = talkDB_key(useridx)
    print(talkkey)
    db.execute('pragma key="'+talkkey+'"')
    db.execute('PRAGMA cipher_compatibility = 3')
    cur = db.cursor()

    # 테이블 추출할 내용 지정
    # chats
    chatsColname = {'time':'시간', 'sender':'보낸사람', 'type':'타입', 'roomidx':'채팅방 번호', 'text':'메시지', 'url':'파일'}
    chatsRowlist = export(app, cur, 'chats', chatsColname, ulist, path) # talk.db에 chats 테이블 내용 추출
    
    # rooms
    roomsColname = {'roomidx':'채팅방 번호', 'name':'채팅방 인원', 'lastChatTime':'시간', 'lastChatSender':'마지막 보낸사람', 'lastChatType':'타입', 'lastChatText':'마지막 보낸 메시지'}
    roomsRowlist = export(app, cur, 'rooms', roomsColname, ulist) # talk.db에 rooms 테이블 내용 추출
    
    # lastindex
    indexColname = {'roomidx':'채팅방 번호', 'lastidx':'마지막 메시지 전송 레코드 번호', 'lastdelidx':'마지막으로 삭제된 메시지 레코드 번호'}
    indexRowlist = export(app, cur, 'lastindex', indexColname) # talk.db에 lastindex 테이블 내용 추출
    
    # sqlite_sequence
    seqColname = {'name':'테이블 이름', 'seq':'레코드 개수'}
    seqRowlist = export(app, cur, 'sqlite_sequence', seqColname) # talk.db에 lastindex 테이블 내용 추출
    
    colname = [chatsColname.values(), roomsColname.values(), indexColname.values(), seqColname.values()]
    rowlist = [chatsRowlist, roomsRowlist, indexRowlist, seqRowlist]

    return colname, rowlist

# lysn data 변환
def lysnConversation(row, colname, col_defs, compare, path):
    d_row=[]
    for en, kr in colname.items():
        value = row[col_defs[en]]
        # 시간 변환
        if kr == '시간' and value != None:
            value = "20"+str(str(value[0:2])+"-" + str(value[2:4])+"-" 
            + str(value[4:6])+" " + str(value[6:8])+":" + str(value[8:10])+":" + str(value[10:12]))
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

def tongtong_gcmDB(path):
    app = 'TongTong'

    # db 열기
    dbfile = path + 'databases/gcm.db'
    
    db = sqlcipher.connect(dbfile)
    cur = db.cursor()
    
    # 테이블 추출할 내용 지정
    # chatting
    chattingColname = {'date' : '시간', 'userId' : '유저 고유 아이디', 'msg' : '메시지', 'name' : '보낸사람', 'thumbnailPath':'사진', 'videoPath':'비디오'}
    chattingRowlist = export(app, cur, 'chatting', chattingColname, None, path)  # gcm.db에 chatting 테이블 내용 추출

    # chatRoomList
    roomColname = {'roomName':'채팅방 이름', 'date' : '시간', 'userId' : '유저 고유 아이디', 'msg' : '마지막 메시지', 'name' : '마지막 보낸사람'}
    roomRowlist = export(app, cur, 'chatRoomList', roomColname)  # gcm.db에 chatting 테이블 내용 추출

    # contact
    contactColname = {'name': '친구 이름', 'phone': '핸드폰 번호'}
    contactRowlist = export(app, cur, 'contacts', contactColname)  # gcm.db에 contact 테이블 내용 추출

    colname = [chattingColname.values(), roomColname.values(), contactColname.values()]
    rowlist = [chattingRowlist, roomRowlist, contactRowlist]

    return colname, rowlist


# TongTong data 변환
def tongtongConversation(row, colname, col_defs, path):
    d_row = []
    for en, kr in colname.items():
        value = row[col_defs[en]]
        if en == 'userId':
            userId = row[col_defs[en]]
        elif en == 'msg' and userId != '':
            enc_msg = row[col_defs[en]]
            value = tong_dec(userId, enc_msg)
            
        # 미디어 파일 추출
        elif kr == '사진' and value != '' and value != None:
            s=value.split('/')
            value=path+'TongMedia/'+s[-2]+'/'+s[-1]

        elif kr == '비디오' and value != '' and value != None:
            s=value.split('/')
            value=path+'TongVideo/'+s[-2]+'/'+s[-1]

        d_row.append(value)

    return d_row

def wickrDB(path, password):
    app = 'Wickr'

    f=open(path+'files/sk.wic', 'rb+')
    skdata = f.read()
    f.close()

    wickrkey = wickrDB_key(skdata, password) # user.db key 구하기
    print(wickrkey)
    # db 열기
    dbfile = path + 'databases/wickr_db'
    db = sqlcipher.connect(dbfile)
    db.execute('pragma key="'+wickrkey+'"')
    db.execute('PRAGMA cipher_compatibility = 4')
    cur = db.cursor()
    
    # 테이블 추출할 내용 지정
    # Wickr_Message
    messageColname = {'timestamp':'시간','messagePayload':'보낸사람','cachedText':'메시지','type':'타입','media':'미디어'}
    messageRowlist = export(app, cur, 'Wickr_Message', messageColname, None, path)  # wickr_db에 Wickr_Message 테이블 내용 추출

    # Wickr_User
    userColname = {'customName':'닉네임', 'userAlias':'사용자 ID','lastActivityTime':'마지막 활동시간'} #,'userImageSecure':'프로필 사진'
    userRowlist = export(app, cur, 'Wickr_User', userColname, None, path)  # wickr_db에 Wickr_User 테이블 내용 추출

    
    colname = [messageColname.values(), userColname.values()]
    rowlist = [messageRowlist, userRowlist]

    return colname, rowlist

# TongTong data 변환
def WickrConversation(row, colname, col_defs, path=None):
    d_row = []
    flag = 0

    for en, kr in colname.items():
        if en != 'type' and en != 'media':
            value = row[col_defs[en]]
        # 시간 변환
        if (kr == '시간' or kr == '마지막 활동시간') and value != None:
            value = datetime.datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
        elif kr == '보낸사람':
            a=value.find(b'\x12')
            username = value[2:a]
            try:
                value=username.decode()
                type = 'text'
            except: # 변환안되면 미디어 파일
                flag = 1
                mdkdata = value

                # type 구하기
                try: # 사진
                    a=mdkdata.find(b'\x0A\x0A')
                    aa=mdkdata.find(b'\x12', a)
                    type = mdkdata[a+2:aa].decode()
                    mdkdata = mdkdata[aa+2:]
                except: # 동영상
                    b=mdkdata.find(b'\x0A\x09')
                    bb=mdkdata.find(b'\x12', b)
                    type = mdkdata[b+2:bb].decode()
                    mdkdata = mdkdata[bb+2:]
                
                # filename, mdk 구하기
                s=(mdkdata.find(b'\x18'))
                c=(mdkdata.find(b'\x2A\x24'))
                d=(mdkdata.find(b'\x32\x21\x00'))
                e=(mdkdata.find(b'\x3A\x80\x01'))

                decfilename = (mdkdata[:s]).decode()
                encfilename=(mdkdata[c+2:d]).decode()
                mdk=(mdkdata[d+3:e])

                # 보낸사람 구하기
                f=value.find(b'\x2A')
                value = value[2:f].decode()

        elif en == 'type':
            value = type          

        elif en == 'media':
            if flag == 0:
                value = ''
            else:
                # 복호화 미디어 파일 저장
                mediaPath = path + 'files/enc/' + encfilename
                mediafile = wickr_media(mdk, mediaPath)
                
                os.makedirs(path+'files/dec',exist_ok=True)
                value = decfilename
                f = open(path +'files/dec/'+value, 'wb+')
                f.write(mediafile)
                f.close()

        d_row.append(value)
        
    return d_row

# Lysn, TongTong 내용 추출하기
def export(app, cur, table, colname, compare=None, mediaPath=None):
    cur.execute('pragma table_info('+table+')')
    rows = cur.fetchall()
    col_defs = { row[1]: row[0] for row in rows }

    cur.execute("SELECT * FROM "+table)
    rows = cur.fetchall()

    # 추출할 내용에 따라 각 행 내용을 리스트로 저장하기
    if app == 'lysn':
        rowlist = [lysnConversation(row,colname,col_defs,compare,mediaPath) for row in rows]
    elif app == 'TongTong':
        rowlist = [tongtongConversation(row,colname,col_defs,mediaPath) for row in rows]
    elif app == 'Wickr':
        rowlist = [WickrConversation(row,colname,col_defs,mediaPath) for row in rows]

    return rowlist




if __name__ == '__main__':
    
    
    '''
    path = "C:/AppData/SM-G955N/Lysn/"
    android_id = '4b0629381a2249a5'
    #android_id = '4f77d977f3f1c488' 
    colnames, rowlists = lysn_userDB(path, android_id)
    colnames, rowlists = lysn_talkDB(path, android_id,rowlists)
    
    print(colnames[0])
    #print(rowlists[0][4])
    for row in rowlists[0]:
        print(row)
    
    '''
    path = "C:/AppData/SM-G955N/TongTong/"
    colnames, rowlists = tongtong_gcmDB(path)
    
    print(colnames[0])
    for row in rowlists[0]:
        print(row)
   
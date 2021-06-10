from pysqlcipher3 import dbapi2 as sqlcipher
from lysn_key import userDB_key, talkDB_key
from wechat_key import wechat_en, wechat_path, wechat_ua, wechat_imei
import os
import hashlib
from Crypto.Cipher import AES
import base64
import time
from datetime import datetime

def wechat_db(path):
    app = 'wechat'

    dbfile = path + 'MicroMsg/' + wechat_path() + '/EnMicroMsg.db'
    #mediaPath = path + '/media'
    imei = wechat_imei()
    uin = wechat_ua()
    db = sqlcipher.connect(dbfile)
    db.execute('pragma key="'+ wechat_en(uin, imei) +'"')
    db.execute('PRAGMA cipher_page_size = 1024;')
    db.execute('PRAGMA cipher_use_hmac = OFF;' )
    db.execute('PRAGMA kdf_iter = 4000;')
    cur = db.cursor()
    
    encolname = {'type' : '파일타입', 'isSend' : '수/발신' , 'talker' : '채팅방에 있는 유저ID', 'createTime' : '보낸 시간' , 'content' : '메세지', 'imgPath' : '이미지'}
    enrowlist = export(app, cur, 'message', encolname)

    colname = [encolname.values()]
    rowlist = [enrowlist]

    return colname, rowlist

def wechatConversation(row, colname, col_defs, compare, mediaPath):
    d_row=[]
    for en, kr in colname.items():
        value = row[col_defs[en]]
        
        if kr == '파일타입':
            if value == 1:
                value = '메세지'
            elif value == 3:
                value = '사진'
            elif value == 43:
                value = '영상'
            elif value == 34:
                value = '음성 메세지'
            elif value == 10000:
                value = '시스템 공지'
            else :
                pass
        
        elif kr == '수/발신':
            if value == 0 :
                value = '수신'
            elif value == 1:
                value = '발신'
            else :
                pass
        
        elif kr == '보낸 시간':
            unixTimestamp = value/1000
            value = datetime.fromtimestamp(int(unixTimestamp))
                
                
        elif kr == '메세지':
            if value == None or len(value) >= 200:
                value = ''
            elif 'wxid' in value :
                value = '미디어 파일' 
                pass
                
        elif kr == '이미지' :
            if value == None:
                value = ''
            else :
                pass
        d_row.append(value)

    return d_row
    
# lysn user.db 내용 추출 
def lysn_userDB(path, android_id):
    app = 'lysn'      
    #userkey = userDB_key(android_id) # user.db key 구하기
    userkey = userDB_key('073ba681a84bea93')
    # db 열기
    #dbfile = path + 'user.db'
    db = sqlcipher.connect("/home/ubuntu2/05_19/05_19/MessengerDecryptedModule--Lysn/AppData/SM-N976N/Lysn/com.everysing.lysn/databases/user.db")
    db.execute('pragma key="'+userkey+'"')
    db.execute('PRAGMA cipher_compatibility = 3')
    cur = db.cursor()
    # db 열기
    #db = sqlcipher.connect(dbfile)
    #db.execute('pragma key="'+userkey+'"')
    #cur = db.cursor()
    
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
def lysn_talkDB(path, android_id):
    app = 'lysn'
    dbfile = path + 'databases/talk.db'
    mediaPath = path + 'LysnMedia/'
    
    # user.db 먼저 열어서 useridx 값 받아오기
    #udbfile=dbfile.replace('talk.db', 'user.db')
    ulists = lysn_userDB(path, android_id)[1]
    ulist = ulists[0]
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
    chatsColname = {'time':'시간', 'sender':'보낸사람', 'type':'타입', 'roomidx':'채팅방 번호', 'text':'메시지', 'thumburl':'파일'}
    chatsRowlist = export(app, cur, 'chats', chatsColname, ulist, mediaPath) # talk.db에 chats 테이블 내용 추출
    
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
def lysnConversation(row, colname, col_defs, compare, mediaPath):
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

        # 미디어 파일 추출
        elif kr == '파일' and mediaPath != None:
            filelist = os.listdir(mediaPath)
            for file in filelist:
                if file == value:
                    print(file)
                    f = open(mediaPath + file, 'rb')
                    value = f.read()
                    f.close()
        d_row.append(value)

    return d_row

def tongtong_gcmDB(path):
    app = 'TongTong'

    # db 열기
    dbfile = path + '/gcm.db' # 요부분
    db = sqlcipher.connect(dbfile)
    cur = db.cursor()

    # 테이블 추출할 내용 지정
    # chatting
    chattingColname = {'msg' : '메시지', 'date' : '시간', 'name' : '보낸사람', 'userId' : '유저 고유 아이디'}
    chattingRowlist = export(app, cur, 'chatting', chattingColname)  # gcm.db에 chatting 테이블 내용 추출

    # contact
    contactColname = {'name': '친구 이름', 'phone': '핸드폰 번호'}
    contactRowlist = export(app, cur, 'contacts', contactColname)  # gcm.db에 contact 테이블 내용 추출

    colname = [chattingColname.values(), contactColname.values()]
    rowlist = [chattingRowlist, contactRowlist]

    return colname, rowlist


# TongTong data 변환
def tongtongConversation(row, colname, col_defs, compare, mediaPath):
    d_row = []
    flag = 0
    for en, kr in colname.items():
        value = row[col_defs[en]]
        if en == 'msg':
            enc_msg = row[col_defs[en]]
            flag = 1
        elif en == 'userId':
            userId = row[col_defs[en]]
        d_row.append(value)

    if flag == 1:
        dec_msg = base64.b64decode(enc_msg)
        concat_userid = (userId + "*" + userId).encode()
        decode1 = hashlib.sha256(concat_userid).digest()
        decode2 = base64.b64encode(decode1)
        key = hashlib.sha256(decode2).digest()
        iv = hashlib.md5(decode2).digest()
        Cipher = AES.new(key, AES.MODE_CBC, iv)
        dec = Cipher.decrypt(dec_msg)
        dec_msg = dec[:-1 * dec[-1]]
        dec_msg = dec_msg.decode()
        d_row[0] = dec_msg


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

    if app == 'TongTong':
        rowlist = [tongtongConversation(row,colname,col_defs,compare,mediaPath) for row in rows]

    if app == 'wechat':
        rowlist = [wechatConversation(row, colname, col_defs,compare,mediaPath) for row in rows]
        
    return rowlist



if __name__ == '__main__':
    
    path = "/home/ubuntu2/05_19/05_19/MessengerDecryptedModule--Lysn/GUI/Wechat/MicroMsg/8a9b2f166cceabe5796650e90955f134"
    #android_id = '073ba681a84bea93' #여기는 리즌파트니까 따로 신경안써도 될듯함
    '''
    colnames, rowlists = lysn_userDB(path, android_id)
    
    print(colnames[0])
    for row in rowlists[0]:
        print(row)
    '''
   
    colnames, rowlists = wechat_db(path)
    
    print(colnames[1])
    for row in rowlists[1]:
        print(row)
    

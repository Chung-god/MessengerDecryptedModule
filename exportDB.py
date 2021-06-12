from pysqlcipher3 import dbapi2 as sqlcipher

import os
import datetime
import time
import json
import xml.etree.ElementTree as elemTree
from requests import get
from datetime import datetime
from lysn_key import userDB_key, talkDB_key
from tong_decrypt import tong_dec
from wickr_decrypt import wickrDB_key, wickr_media
from kakao_decrypt import decrypt
from purple_decrypt import purple_dec
from wechat_key import wechat_en, wechat_path, wechat_ua, wechat_imei

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
    
    db.execute('pragma key="'+talkkey+'"')
    db.execute('PRAGMA cipher_compatibility = 3')
    cur = db.cursor()

    # 테이블 추출할 내용 지정
    # chats
    chatsColname = {'time':'시간', 'sender':'보낸사람', 'roomidx':'채팅방 번호', 'type':'타입', 'text':'메시지', 'url':'파일'}
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
    # chatRoomList
    roomColname = {'roomKey':'채팅방 번호', 'roomName':'채팅방 이름', 'date' : '마지막 보낸 시간', 
                    'userId' : '유저 고유 아이디', 'member':'채팅방 인원', 'msg' : '마지막 메시지'}
    roomRowlist = export(app, cur, 'chatRoomList', roomColname)  # gcm.db에 chatting 테이블 내용 추출

    # chatting
    chattingColname = {'date':'시간', 'userId':'유저 고유 아이디', 'name':'보낸사람', 'roomKey':'채팅방 번호', 
                        'msgType':'타입', 'msg':'메시지', 'thumbnailPath':'사진', 'videoPath':'비디오'}
    chattingRowlist = export(app, cur, 'chatting', chattingColname, roomRowlist, path)  # gcm.db에 chatting 테이블 내용 추출

    # friend
    friendColname = {'userId': '유저 고유 아이디', 'name':'이름', 'phoneNumber': '핸드폰 번호'}
    friendRowlist = export(app, cur, 'friendsList', friendColname)  # gcm.db에 contact 테이블 내용 추출

    colname = [chattingColname.values(), roomColname.values(), friendColname.values()]
    rowlist = [chattingRowlist, roomRowlist, friendRowlist]

    return colname, rowlist


# TongTong data 변환
def tongtongConversation(row, colname, col_defs, compare, path):
    d_row = []
    for en, kr in colname.items():
        value = row[col_defs[en]]
        if value == None: value = ''

        if en == 'userId':
            userId = value
        elif en == 'msg' and userId != '':
            enc_msg = value
            value = tong_dec(userId, enc_msg)
        elif en == 'msgType':
            if value == 0: value = 'text'
            elif value == 1: value = 'image'
            elif value == 2: value = 'video'
            elif value == 4: value = 'audio'
            else: value = 'etc'

        # 미디어 파일 추출
        elif kr == '사진' and value != '':
            s=value.split('/')
            value=path+'TongMedia/'+s[-2]+'/'+s[-1]
        elif kr == '비디오' and value != '':
            s=value.split('/')
            value=path+'TongVideo/'+s[-2]+'/'+s[-1]
        elif en == 'roomName':
            roomName = value
        elif en == 'member':
            names = []
            if value == '':
                value = roomName
            else:
                value=json.loads(value)
                for data in value:
                    names.append(data['name'])
                nameList = [data['name'] for data in value]
                value = ', '.join(nameList)
        
        d_row.append(value)

    return d_row

def wickrDB(path, password):
    app = 'Wickr'

    f=open(path+'files/sk.wic', 'rb+')
    skdata = f.read()
    f.close()

    wickrkey = wickrDB_key(skdata, password)
    print(wickrkey)

    # db 열기
    dbfile = path + 'databases/wickr_db'
    db = sqlcipher.connect(dbfile)
    db.execute('pragma key="'+wickrkey+'"')
    db.execute('PRAGMA cipher_compatibility = 4')
    cur = db.cursor()
    
    # 테이블 추출할 내용 지정
    # Wickr_Message
    messageColname = {'timestamp':'시간','messagePayload':'보낸사람', 'vGroupID':'채팅방', 'type':'타입', 'cachedText':'메시지','media':'미디어'}
    messageRowlist = export(app, cur, 'Wickr_Message', messageColname, None, path)  # wickr_db에 Wickr_Message 테이블 내용 추출

    # Wickr_User
    userColname = {'serverIDHash':'유저 해시값','customName':'닉네임', 'userAlias':'사용자 ID','lastActivityTime':'마지막 활동시간'} #,'userImageSecure':'프로필 사진'
    userRowlist = export(app, cur, 'Wickr_User', userColname, None, path)  # wickr_db에 Wickr_User 테이블 내용 추출
    
    # Wickr_ConvoUser
    convuserColname = {'vGroupID':'cvu 채팅방 번호', 'serverIDHash':'사용자 ID'} #,'userImageSecure':'프로필 사진'
    convuserRowlist = export(app, cur, 'Wickr_ConvoUser', convuserColname, userRowlist, path)  # wickr_db에 Wickr_User 테이블 내용 추출

    # Wickr_Convo
    convoColname = {'vGroupID':'채팅방 번호', 'chatRoom':'채팅방 인원'} #,'userImageSecure':'프로필 사진'
    convoRowlist = export(app, cur, 'Wickr_Convo', convoColname, convuserRowlist, path)  # wickr_db에 Wickr_User 테이블 내용 추출

    colname = [messageColname.values(), userColname.values(), convoColname.values()]
    rowlist = [messageRowlist, userRowlist, convoRowlist]

    return colname, rowlist

# Wickr data 변환
def WickrConversation(row, colname, col_defs, compare, path=None):
    d_row = []
    flag, flag2 = 0, 0
    msg = ''
    for en, kr in colname.items():
        if en != 'type' and en != 'media' and en != 'chatRoom':
            value = row[col_defs[en]]
        if value == None: value = ''

        # 시간 변환
        if (kr == '시간' or kr == '마지막 활동시간') and value != '':
            value = datetime.datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
        elif kr == '메시지':
            msg = value
        elif kr == '보낸사람':
            a=value.find(b'\x12',2)
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
                    try:
                        b=mdkdata.find(b'\x0A\x09')
                        bb=mdkdata.find(b'\x12', b)
                        type = mdkdata[b+2:bb].decode()
                        mdkdata = mdkdata[bb+2:]
                    except:
                        value = 'Wickr'
                        type = 'etc'
                        flag=0
                        flag2 = 1
                        
                if flag2 == 0:
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
        
        elif en == 'serverIDHash' and kr == '사용자 ID':
            for ulist in compare:
                if value == ulist[0]:   
                    value = ulist[2]

        elif kr == '채팅방 번호':
            for cp in compare:
                if cp[0] == value:
                    chatnames = [cp[1] for cp in compare if cp[0] == value]
        elif en == 'chatRoom':
            value = ', '.join(chatnames)
            
        d_row.append(value)

    if msg == '':
        d_row[1] = d_row[1][:-2]
        
    return d_row


def purple_DB(path):
    app = 'Purple'

    # db 열기
    dbfile = path + 'databases/Commuity.db'
    os.makedirs(path+'purpleMedia', exist_ok=True)

    db = sqlcipher.connect(dbfile)
    cur = db.cursor()

    # 테이블 추출할 내용 지정
    # limemessage
    chattingColname = {'dateTime': '시간', 'senderCharacterName': '보낸사람', 
                        'groupId':'그룹 ID', 'messageType': '타입', 'content': '메시지', 'optional': '파일'}
    chattingRowlist = export(app, cur, 'limemessage', chattingColname, None, path)  # Commuity.db에 chatting 테이블 내용 추출

    # limegroupuserinfo
    roomUserColname = {'groupId': '그룹 ID user', 'characterName':'그룹 유저'}
    roomUserRowlist = export(app, cur, 'limegroupuserinfo', roomUserColname, None, path)
    
    # limegroupownerinfo
    roomOwnerColname = {'groupId': '그룹 ID owner', 'ownerCharacterName':'그룹 소유자', 'groupMember':'그룹 멤버'}
    roomOwnerRowlist = export(app, cur, 'limegroupownerinfo', roomOwnerColname, roomUserRowlist, path)

    # limegroup
    roomColname = {'groupId': '그룹 고유 ID', 'gameChannelType':'채널 타입', 'name':'그룹 이름', 'member':'그룹 인원', 
                    'groupImage':'그룹 프로필 이미지', 'dateCreated': '마지막 보낸 시간', 'lastMessageContent': '마지막 보낸 메세지'}
    roomRowlist = export(app, cur, 'limegroup', roomColname, roomOwnerRowlist, path)

    # sqlite_sequence
    seqColname = {'name': '테이블 이름', 'seq': '레코드 개수'}
    seqRowlist = export(app, cur, 'sqlite_sequence', seqColname, None, path)
    
    colname = [chattingColname.values(), roomColname.values(), seqColname.values()]
    rowlist = [chattingRowlist, roomRowlist, seqRowlist]

    return colname, rowlist


def purpleConversation(row, colname, col_defs, compare, path):
    d_row = []
    for en, kr in colname.items():
        if en != 'groupMember' and en != 'member':
            value = row[col_defs[en]]
        if value == None: value = ''

        # 메시지 복호화
        if en == 'content' and value != '':
            tree = elemTree.parse(path + 'shared_prefs/NC Community.xml')
            user = tree.find('./string[@name="shared_appsflyer_user_id"]')
            user = user.text.replace('_mobilepurple', '')
            value = purple_dec(user, value)
        # 그룹 인원 구하기
        elif kr == '그룹 ID owner': groupidowner = value
        elif kr == '그룹 소유자': groupowner = value
        elif kr == '그룹 멤버':
            value = [ulist[1] for ulist in compare if groupidowner == ulist[0]]
            value.append(groupowner)
            value = ', '.join(value)
        elif kr == '그룹 고유 ID': groupid = value
        elif kr == '채널 타입': 
            if value == '': value = 'NORMAL'
            channeltype = value
        elif kr == '그룹 이름': groupname = value
        elif en == 'member':
            if channeltype == 'WORLD':
                value = groupname
            else:
                for olist in compare:
                    if groupid == olist[0]:   
                        value = olist[2]
        # 시간
        elif kr == '시간' or kr == '마지막 보낸 시간':
            value = datetime.datetime.fromtimestamp(value / 1000).strftime('%Y-%m-%d %H:%M:%S')  
        # 미디어     
        elif en == 'groupImage' and value != '':
            imageUrl = value
            s=imageUrl.split('/')
            iname = s[-1]         
        elif en == 'messageType':
            msgtype = value
        elif en == 'optional' and value != '':
            # path 구하기
            if msgtype == 'IMAGE':
                image=json.loads(value)[0]
                imageUrl=image['downloadUrl']
                s=imageUrl.split('/')
                iname = s[-1]+'.jpg'
            elif msgtype == 'NEMO':
                image=json.loads(value)
                imageUrl=image['url']
                s=imageUrl.split('/')
                iname = s[-2]+'_'+s[-1]+'.jpg'    
            else:
                value = ''
        # url 파일 저장
        if en == 'groupImage' or en == 'optional':
            if value != '':
                try:
                    value = path + 'purpleMedia/' + iname
                    with open(value, 'wb') as file:
                        response = get(imageUrl)
                        file.write(response.content)
                except:
                    value = path + 'purpleMedia/' + iname

        d_row.append(value)

    return d_row

def KaKaoTalk_DB_1(path):
    app = 'KakaoTalk'

    # db 열기
    dbfile = path + 'databases/KakaoTalk.db'
    db = sqlcipher.connect(dbfile)
    cur = db.cursor()

    chat_logsColname = {'message' : '메시지','user_id':'보낸 사람', 'created_at' : '생성'}
    chat_logsRowlist = export(app, cur, 'chat_logs', chat_logsColname)  
    
    # KakaoTalk.db에 chat_logs 테이블 내용 추출
    colname = [chat_logsColname.values()]
    rowlist = [chat_logsRowlist]
    
    return colname, rowlist

def KaKaoTalk_DB_2(path):
    app = 'KakaoTalk'

    #db 열기
    dbfile = path + 'databases/KakaoTalk2.db'
    db = sqlcipher.connect(dbfile)
    cur = db.cursor()

    friendsColname = {'id' : '아이디', 'name' : '사용자'}
    friendsRowlist = export(app, cur, 'friends', friendsColname) 

    colname = [friendsColname.values()]
    rowlist = [friendsRowlist]

    return colname, rowlist
    
def kakaoConversation(row, colname, col_defs, compare=None, mediaPath=None):
    d_row = []
    flag=0
    for en, kr in colname.items():
        value = row[col_defs[en]]
            
        if en == 'message' and value != '':
            enc_msg = value
            flag = 1
        elif en == 'user_id' and value != '':
            xid = value
        d_row.append(value)

    if flag == 1:
        d_row[0] = decrypt(xid, enc_msg)

    return d_row

def wechat_db(path):
    app = 'Wechat'

    dbfile = path + 'MicroMsg/' + wechat_path() + '/EnMicroMsg.db'
    mediaPath = path + '/media'
    imei = wechat_imei()
    uin = wechat_ua()
    db = sqlcipher.connect(dbfile)

    db.execute('pragma key="' + wechat_en(uin, imei) + '"')
    db.execute('PRAGMA cipher_compatibility = 3')
    db.execute('PRAGMA cipher_use_hmac = OFF;')
    db.execute('PRAGMA cipher_page_size = 1024;')
    db.execute('PRAGMA kdf_iter = 4000;')

    cur = db.cursor()

    encolname = {'type': '파일타입', 'isSend': '수/발신', 'talker': '채팅방에 있는 유저ID', 'createTime': '보낸 시간', 'content': '메세지',
                 'imgPath': '이미지'}
    enrowlist = export(app, cur, 'message', encolname)

    colname = [encolname.values()]
    rowlist = [enrowlist]

    return colname, rowlist


def wechatConversation(row, colname, col_defs, compare, mediaPath):
    d_row = []
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
            else:
                pass

        elif kr == '수/발신':
            if value == 0:
                value = '수신'
            elif value == 1:
                value = '발신'
            else:
                pass

        elif kr == '보낸 시간':
            unixTimestamp = value / 1000
            value = datetime.fromtimestamp(int(unixTimestamp))


        elif kr == '메세지':
            if value == None or len(value) >= 200:
                value = ''
            elif 'wxid' in value:
                value = '미디어 파일'
                pass

        elif kr == '이미지':
            if value == None:
                value = ''
            else:
                pass
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
        rowlist = [tongtongConversation(row,colname,col_defs,compare,mediaPath) for row in rows]
    elif app == 'Wickr':
        rowlist = [WickrConversation(row,colname,col_defs,compare,mediaPath) for row in rows]
    elif app == 'KakaoTalk':
        rowlist = [kakaoConversation(row,colname,col_defs,mediaPath) for row in rows]
    elif app == 'Purple':
        rowlist = [purpleConversation(row, colname, col_defs, compare, mediaPath) for row in rows]
    elif app == "Wechat":
        rowlist = [wechatConversation(row, colname, col_defs, compare, mediaPath) for row in rows]

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
    
    
    path = "C:/AppData/SM-G955N/TongTong/"
    colnames, rowlists = tongtong_gcmDB(path)
    
    print(colnames[0])
    for row in rowlists[0]:
        print(row)
    
    
    path = "C:/AppData/SM-G955N/KakaoTalk/"
    colnames, rowlists = KaKaoTalk_DB_1(path)
    
    print(colnames[0])
    for row in rowlists[0]:
        print(row)
    
    
    path = "C:/AppData/SM-G955N/W/"
    password = 'dltndk11@@'
    colnames, rowlists = wickrDB(path, password)
    
    print(colnames[0])
    for row in rowlists[0]:
        print(row)
    '''

    path = "C:/AppData/SM-G955N/PurPle/"
    colnames, rowlists = purple_DB(path)
    
    print(colnames[1])
    for row in rowlists[1]:
        print(row)
        
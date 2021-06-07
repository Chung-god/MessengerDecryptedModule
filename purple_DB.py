# -*- coding: utf-8 -*-
from pysqlcipher3 import dbapi2 as sqlcipher
from Crypto.Cipher import AES
import hashlib
import base64
import os
import datetime
import time
import xml.etree.ElementTree as elemTree
from purple_decrypt import purple_dec

def export(app, cur, table, colname, compare=None, mediaPath=None):
    cur.execute('pragma table_info('+table+')')
    rows = cur.fetchall()
    col_defs = { row[1]: row[0] for row in rows }

    cur.execute("SELECT * FROM "+table)
    rows = cur.fetchall()

    if app == 'Purple':
        rowlist = [purpleConversation(row,colname,col_defs,mediaPath) for row in rows]

    return rowlist

db = sqlcipher.connect('Commuity.db')
cur = db.cursor()


def purple_DB(path):
    app = 'Purple'

    # db 열기
    dbfile ='databases/Commuity.db'

    db = sqlcipher.connect(dbfile)
    cur = db.cursor()

    # 테이블 추출할 내용 지정
    # chatting
    chattingColname = {'dateTime': '시간', 'senderGameUserId': '유저 고유 아이디', 'content': '메시지',
                       'senderCharacterName': '보낸사람', 'optional': '이미지다운로드', 'messageType':'타입'}
    chattingRowlist = export(app, cur, 'limemessage', chattingColname, None, 'Commuity.db')  # Commuity.db에 chatting 테이블 내용 추출

    # chatRoomList
    roomColname = {'groupId': '그룹 고유 ID', 'dateCreated': '시간', 'lastMessageContent': '마지막 보낸 메세지', 'name': '마지막 보낸 사람'}
    roomRowlist = export(app, cur, 'limegroup', roomColname, None, 'Commuity.db')

    # sqlite_sequence
    seqColname = {'name': '테이블 이름', 'seq': '레코드 개수'}
    seqRowlist = export(app, cur, 'sqlite_sequence', seqColname, None, 'Commuity.db')
    colname = [chattingColname.values(), roomColname.values(), seqColname.values()]
    rowlist = [chattingRowlist, roomRowlist, seqRowlist]

    return colname, rowlist


def purpleConversation(row, colname, col_defs, path=None):
    d_row = []
    for en, kr in colname.items():
        value = row[col_defs[en]]
        if en == 'content' and value!='':
            enc_msg = row[col_defs[en]]
            # value = purple_dec(userId, enc_msg)
            tree = elemTree.parse('/home/ksjr/PurPle/PurPle/shared_prefs/NC Community.xml')
            user = tree.find('./string[@name="shared_appsflyer_user_id"]')
            user = user.text.replace('_mobilepurple', '')
            value = purple_dec(user, enc_msg)
        elif kr == '시간':
            t = time.localtime(value/1000)
            value = str(t.tm_year) + "-" + str(t.tm_mon) + "-" + str(t.tm_mday) + " "+ str(t.tm_hour) + ":" + str(t.tm_min) + ":"+ str(t.tm_sec)
        elif en == 'optional' and value!='' and value!='':
            try:
                index = value.find('downloadUrl')
                if(index != -1):
                    i = index + 14
                    strURL = ''
                    while (value[i] != '"'):
                        strURL += value[i]
                        i = i + 1
                    value = strURL
                else:
                    value = ''
            except:
                value = ''
                d_row.append(value)

        d_row.append(value)
    
    return d_row


if __name__ == '__main__':
    path = ''
    colnames, rowlists = purple_DB(path)

    print(colnames[0])
    for row in rowlists[0]:
        print(row)
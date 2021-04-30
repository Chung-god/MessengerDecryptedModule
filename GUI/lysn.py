from pysqlcipher3 import dbapi2 as sqlcipher
from lysn_key import userDB_key, talkDB_key

def lysn_userDB(dbfile, android_id):
    userkey = userDB_key(android_id)
    db = sqlcipher.connect(dbfile)
    db.execute('pragma key="'+userkey+'"')
    cur = db.cursor()

    colname = {'username':'이름', 'useridx':'고유 번호(idx)', 'userId':'이메일', 'phoneNo':'핸드폰 번호', 'inviteName':'친구 신청시 표시되는 문구'}
    rowlist = export(cur, 'users', colname)
    return colname.values(), rowlist

# useridx = "2169372"
def lysn_talkDB(dbfile, android_id):
    udbfile=dbfile.replace('talk.db', 'user.db')
    ulist = lysn_userDB(udbfile, android_id)[1]
    useridx = ulist[0][1]

    db = sqlcipher.connect(dbfile)
    talkkey = talkDB_key(useridx)
    db.execute('pragma key="'+talkkey+'"')
    
    cur = db.cursor()
    colname = {'time':'시간', 'sender':'보낸사람', 'type':'타입', 'roomidx':'채팅방 번호', 'text':'메시지'}
    rowlist = export(cur, 'chats', colname)
    return colname.values(), rowlist

def export(cur, table, colname):
    cur.execute('pragma table_info('+table+')')
    rows = cur.fetchall()
    col_defs = { row[1]: row[0] for row in rows }

    cur.execute("SELECT * FROM "+table)
    rows = cur.fetchall()

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
    
      
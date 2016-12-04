import sqlite3
from pprint import pprint
import os, binascii

def getTables():
    if c != None:
        q = "SELECT name FROM sqlite_master WHERE type='table';"
        c.execute(q)
        list_tableName = map((lambda table: str(table[0])), c.fetchall())
        return list_tableName


def printTable(tableName):
    q = "SELECT * FROM %s;" % tableName
    tableData = c.execute(q).fetchall()
    pprint(tableData)


def setup():
    if 'user' not in getTables():
        q = '''
        CREATE TABLE user (
        id INTEGER PRIMARY KEY,
        username VARCHAR(50) UNIQUE,
        password VARCHAR(50),
        kills INTEGER DEFAULT 0,
        qr VARCHAR(50) UNIQUE,
        target_id INTEGER DEFAULT 0
        );
        '''
        c.execute(q)
        
        q = '''
        CREATE TABLE kill (
        id INTEGER PRIMARY KEY,
        killer_id INTEGER,
        victim_id INTEGER,
        ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        c.execute(q)
        
        oneTimeSetup()
        conn.commit()


def getUserID(username):
    q = "SELECT id FROM user WHERE username=? LIMIT 1;"
    return c.execute(q, (username,)).fetchone()[0] #should be user_id


def getUsername(user_id):
    q = "SELECT username FROM user WHERE id=? LIMIT 1;"
    return c.execute(q, (user_id,)).fetchone()[0]


'''
0 if all ok
1 if username empty
2 if password empty
3 if username doesn't exist
4 if username DOES exist but wrong password
'''
def loginAuth(username, password):
    if not username.strip(): #username empty
        return 1
    if not password.strip(): #password empty
        return 2
    if isInDB( ("username", username) ):
        q = "SELECT 1 FROM user WHERE username=? AND password=? LIMIT 1;"
        correctPass = c.execute(q, (username, password)).fetchone()
        if correctPass:
            return 0
        return 4
    return 3



'''
0 if all ok
1 if username empty
2 if pass or rpass empty
3 if passwords don't match
4 if username already exists
'''
def registerAuth(username, password, password_repeat):
    if not username.strip():
        return 1
    if not password.strip() or not password_repeat.strip():
        return 2
    if password != password_repeat:
        return 3
    if isInDB( ("username", username) ):
        return 4
    return 0


def isInDB(*columns,**table):return True if c.execute("SELECT 1 FROM %s WHERE %s LIMIT 1;"%(table["table"]if table else"user",\
reduce((lambda c1,c2:"(%s) AND (%s)"%("%s=\"%s\""%(columns[0][0],columns[0][1])if isinstance(c1,tuple)else c1,"%s=\"%s\""%(c2[0]\
,c2[1]))),columns)if len(columns)-1 else"%s=\"%s\""%(columns[0][0],columns[0][1]))).fetchone() else False

def addUser(username, password):
    q = "SELECT target_id FROM user ORDER BY RANDOM() LIMIT 1"
    targetid = int(c.execute(q).fetchone()[0])
    qr = binascii.b2a_hex(os.urandom(5))
    q = "INSERT INTO user(username, password, target_id, qr) VALUES(?,?,?,?);"
    c.execute(q, (username, password, targetid, qr))
    conn.commit()


def getTargetID(userid):
    q = "SELECT target_id FROM user WHERE id=? LIMIT 1"
    x = c.execute(q, (userid,))
    return int(x.fetchone()[0])

def getQR(userid):
    q = "SELECT qr FROM user WHERE id=? LIMIT 1"
    x = c.execute(q, (userid,)).fetchone()[0]
    return x

def validKill(userid, victimQR):
    victimQR_real = getQR(getTargetID(userid))
    print victimQR_real
    return victimQR == victimQR_real

def oneTimeSetup():
    q = 'INSERT INTO user(username, password, target_id, qr) VALUES("top","kek",1,"f9y8e4uh4");'
    c.execute(q)
    addUser("cop", "tech")

def debug():
    print "\nTESTING USER..."
    print validKill(2, 'f9y8e4uh4')

    print "\nPRINTING USER TABLE..."
    printTable("user")
    printTable("kill")


if __name__ == "__main__":
    conn = sqlite3.connect('testing.db')
    c = conn.cursor()
    setup()
    debug()
else:
    conn = sqlite3.connect('dinohunter.db')
    c = conn.cursor()
    setup()

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
    if getTables() is not None and 'user' not in getTables():
        q = '''
        CREATE TABLE user (
        id INTEGER PRIMARY KEY,
        username VARCHAR(50) UNIQUE,
        password VARCHAR(50),
        kills INTEGER,
        qr VARCHAR(50) UNIQUE
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


def addUser(username, password):
    q = "INSERT INTO user(username, password) VALUES(?,?)"
    c.execute(q, (username, password))
    conn.commit()


def isInDB(*columns,**table):return True if c.execute("SELECT 1 FROM %s WHERE %s LIMIT 1;"%(table["table"]if table else"user",\
reduce((lambda c1,c2:"(%s) AND (%s)"%("%s=\"%s\""%(columns[0][0],columns[0][1])if isinstance(c1,tuple)else c1,"%s=\"%s\""%(c2[0]\
,c2[1]))),columns)if len(columns)-1 else"%s=\"%s\""%(columns[0][0],columns[0][1]))).fetchone() else False


def getTarget(userid):
    q = "SELECT target FROM user WHERE id=?"
    targetid = int(c.execute(q, (userid,))[0])
    return targetid

def validKill(userID, victimQR):
    pass

def generateQR(userid):
    qr = binascii.b2a_hex(os.urandom(15))
    q = "REPLACE INTO user(id, target) VALUES "

def assignTarget(userid):
    q = "SELECT * FROM user WHERE id != ? LIMIT 1"
    targetid = c.execute(q,(userid,))
    
    q = "INSERT INTO user(target) VALUES(?)"
    c.execute(q, (targetid,))

def oneTimeSetup():
    q = "INSERT INTO user(username, password) VALUES(\"top\",\"kek\");"
    c.execute(q)
    q = "INSERT INTO user(username, password) VALUES(\"kop\",\"tech\");"
    c.execute(q)


def debug():
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

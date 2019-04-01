import pymysql
db = pymysql.connect('localhost', 'root', 'root')
cur = db.cursor()
cur.execute('use bankforiegndb')
cur.execute('select max(accno) from login')
rs=cur.fetchone()
if rs[0]==None:
    accno=10000
else:
    accno=rs[0]
def addreg(name,username,password,cpass):

    cur.execute('select username from login where username=%s', (username))
    rs = cur.fetchone()
    if rs == None:
        if password==cpass:
            cur.execute('insert into login(username,password) values(%s,%s)', (username, password))
            cur.execute('insert into register(name) values(%s)', (name))
            id=cur.lastrowid
            cur.execute('update login set fkid=%s where username=%s', (id,username))
            db.commit()
            return('insert successfully\n login to continue')
        else:
            raise IndexError("pasword not match")
    else:
        raise IndexError("user already exists")
def login(username,password):
    cur.execute('select username,password from login where username=%s and password=%s',(username,password))
    rs=cur.fetchone()
    if rs==None:
        raise IndexError('incorrect details')
def updateProf(username,address,phone,atmno,balance):
    global accno
    print(username)
    print(address)
    print(phone)
    print(atmno)
    print(balance)
    cur.execute('select fkid from login where username=%s',(username))
    rs = cur.fetchone()
    id = rs[0]
    print(id)
    cur.execute('select accno from login where username=%s',(username))
    rc = cur.fetchone()
    print('rc',rc)
    cur.execute('select id from login where username=%s', (username))
    rs = cur.fetchone()
    logid = rs[0]
    print('logid', logid)
    if rc[0]==None:
        print('okkk')
    else:
        # raise IndexError('already updated')
        print('failed')
    if rc[0]== None:
        accno = int(accno) + 1
        cur.execute('update register set address=%s,phno=%s,atmno=%s where id=%s', (address, phone, atmno, id))
        db.commit()
        cur.execute('update login set accno=%s where username=%s',(accno,username))
        db.commit()
        cur.execute('select id from login where username=%s',(username))
        rs=cur.fetchone()
        logid=rs[0]
        print('logid',logid)
        cur.execute('insert into balance(balance,fkid) values(%s,%s)',(balance,logid))
        db.commit()
    else:
        raise IndexError('oops!!!you already updated')

def deposit(amount,uname):
    cur.execute('select id from login where username=%s',(uname))
    rs=cur.fetchone()
    print(rs[0])
    cur.execute('select balance from balance where fkid=%s',(rs[0]))
    rc=cur.fetchone()
    print(rc[0])
    amount=int(amount)+rc[0]
    print(amount)
    cur.execute('update balance set balance=%s where fkid=%s',(amount,rs[0]))
    db.commit()
def display(username,passw,atmno):
    cur.execute('select * from login where username=%s',(username))
    rs=cur.fetchone()
    idlog=rs[0]
    passdb=rs[3]
    accno=rs[1]
    fidlog=rs[4]
    print(fidlog)
    cur.execute('select * from register where id=%s',(fidlog))
    rr=cur.fetchone()
    atmdb=rr[4]
    cur.execute('select balance from balance where fkid=%s',(idlog))
    rb=cur.fetchone()
    if passw==passdb and atmno==str(atmdb):
        name=rr[1]
        address=rr[2]
        phno=str(rr[3])
        balance=str(rb[0])
        return name+','+username+','+address+','+phno+','+balance
    else:
        raise AssertionError('password or atmno is wrong')
def propicselector(uname):
    cur.execute('select register.propic from register join login where register.id=login.fkid and login.username=%s',(uname))
    rss=cur.fetchone()
    return rss[0]

def updatepropic(uname,fname):
    cur.execute('select register.propic from register join login where register.id=login.fkid and login.username=%s',
                (uname))
    rs = cur.fetchone()
    print(rs)
    if rs[0]==None:
        cur.execute('select fkid from login where username=%s',(uname))
        rc=cur.fetchone()
        id=rc[0]
        cur.execute('update register set propic=%s where id=%s',(fname,id))
        db.commit()
    else:
        raise FileExistsError("pro pic already updated")
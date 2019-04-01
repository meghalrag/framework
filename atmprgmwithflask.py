from _socket import gaierror
from smtplib import SMTPAuthenticationError

from flask import Flask, redirect, url_for, render_template, request, session, Response, make_response, flash
import os
from FlaskProgram.database.dbconnection import addreg, login, updateProf, deposit, display, propicselector,updatepropic
from flask_mail import Mail,Message

print(os.getcwd())
sess=0

app=Flask('')
mail=Mail(app)

flag=''
app.secret_key='skey'
app.config['SESSION_TYPE']='filesystem'
@app.route('/')
def f1():
    return render_template('html/AtmPrgmFiles/logandsignup.html')
@app.route('/register')
def f2():
    return render_template('html/AtmPrgmFiles/logandsignup.html')
@app.route('/funreg',methods=['post','get'])
def f5():
    password = request.form['password']
    cpass=request.form['cpassword']
    name=request.form['name']
    username=request.form['username']
    if password==cpass:
        try:
            addreg(name,username,password,cpass)
            return render_template('html/AtmPrgmFiles/successreg.html')
        except IndexError as arg:
            return str(arg)+' try again'

    else:
        flash('password not match')
        return render_template('html/AtmPrgmFiles/logandsignup.html')
        # return "password not match try again"
def f3():
    return render_template('html/AtmPrgmFiles/logandsignup.html')
@app.route('/login')
def f4():
    return render_template('html/AtmPrgmFiles/logandsignup.html')
@app.route('/funlog',methods=['post','get'])
def f6():
    global sess
    username=request.form['username']
    password=request.form['password']
    try:
        login(username,password)
        session['username']=username
        # session['pass']=password
        sess=0
        print('sess,',sess)
        a=propicselector(session['username'])
        print(type(a))
        session['proimage'] = str(a)
        return render_template('html/AtmPrgmFiles/home2.html',uname=session['username'],passw=password,img1=session['proimage'])
    except (IOError,IndexError) as arg:
        flash('incorrect details')
        return render_template('html/AtmPrgmFiles/logandsignup.html')
        # return str(arg)
@app.route('/profileupd')
def f7():
    return render_template('html/AtmPrgmFiles/profupdate.html')
@app.route('/updateprof',methods=['post','get'])
def f8():
    address=request.form['address']
    phone=request.form['phone']
    atmno=request.form['atmno']
    balance=request.form['balance']
    try:
        updateProf(session['username'],address,phone,atmno,balance)
        flash('update')
        return render_template('html/AtmPrgmFiles/home2.html',message='update successfully',img1=session['proimage'])
    except (IndexError,KeyError) as arg:
        if  'username' in str(arg):
            return 'error occured while updating...' + "you are already logged out"
        else:
            flash('error')
            return render_template('html/AtmPrgmFiles/home2.html',msg='error occured while updating...'+str(arg),img1=session['proimage'])
@app.route('/logout')
def f9():
    try:
        global sess
        session.pop('username')
        session.pop('proimage')
        session.pop('gmailuser')
        session.pop('gmailpass')
        # session.pop('pass')
        sess=1
        print('sess,', sess)
        print(type(sess))
        return render_template('html/AtmPrgmFiles/logandsignup.html')
    except KeyError as arg:
        return 'you are already logged out click login to login again'+render_template('html/AtmPrgmFiles/logandsignup.html')
@app.route('/returnhome')
def f10():
    try:
        return render_template('html/AtmPrgmFiles/home2.html',uname=session['username'],img1=session['proimage'])
    except KeyError:
        return 'you are already logged out click login to login again'+render_template('html/AtmPrgmFiles/logandsignup.html')
@app.route('/depo',methods=['post','get'])
def f11():
    try:
        amount=request.form['amount']
        camount=request.form['camount']
        if int(amount)==int(camount):
            deposit(amount,session['username'])
            flash('success')
            return render_template('html/AtmPrgmFiles/home2.html',uname=session['username'], msg='cash credited successfully',img1=session['proimage'])
        else:
            flash('error')
            return render_template('html/AtmPrgmFiles/home2.html', msg='please check the amount U entered',img1=session['proimage'])
    except KeyError:
        return 'you are already logged out click login to login again' + render_template(
            'html/AtmPrgmFiles/logandsignup.html')
@app.route('/display',methods=['post','get'])
def f12():
    try:
        passw=request.form['password']
        atmno=request.form['atmno']
        details=display(session['username'],passw,atmno)
        d=details.split(',')
        return render_template('html/AtmPrgmFiles/home2.html',uname=session['username'],flag="1",name=d[0],username=d[1],address=d[2],phone=d[3],bal=d[4],img1=session['proimage'])
    except AssertionError as arg:
        flash('error')
        return render_template('html/AtmPrgmFiles/home2.html', msg=str(arg),img1=session['proimage'])

###########upload image#########################################

# UPLOAD_FOLDER = os.path.basename('static/uploads')
mypath=os.getcwd()
UPLOAD_FOLDER=mypath+'/static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
count=0
@app.route('/proimage',methods=['post','get'])
def f13():
    global count
    try:
        # image=request.form['upload']
        file=request.files['upload']
        count+=1
        # print(file.filename)
        updatepropic(session['username'], file.filename)
        f = os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
        file.save(f)
        session.pop('proimage')
        session['proimage']=file.filename
        return render_template('html/AtmPrgmFiles/home2.html',img1=session['proimage'],uname=session['username'])
    except FileExistsError as arg:
        print(arg)
        flash('error')
        return render_template('html/AtmPrgmFiles/home2.html',msg=str(arg),img1=session['proimage'],uname=session['username'])
##################################################################

######################send email##################################
@app.route('/emailauth',methods=['post','get'])
def f14():
    usern = request.form['usern']
    passw = request.form['passw']
    print(usern,passw)
    session['gmailuser'] = usern
    session['gmailpass'] = passw
    return render_template('html/AtmPrgmFiles/home2.html',img1=session['proimage'],uname=session['username'],ff='text')
@app.route('/email',methods=['post','get'])
def f15():
    text=request.form['text']
    try:
        print('g',session['gmailuser'])
        print('p',session['gmailpass'])
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USERNAME'] = session['gmailuser']
        app.config['MAIL_PASSWORD'] = session['gmailpass']
        app.config['MAIL_USE_TLS'] = False
        app.config['MAIL_USE_SSL'] = True
        mail = Mail(app)

        msg = Message('complaint', sender=session['gmailuser'], recipients=['meghalrag02@gmail.com'])
        msg.body = text
        mail.send(msg)
        flash('success')
        return render_template('html/AtmPrgmFiles/home2.html', uname=session['username'], msg='your complaint is submitted...we will contact you within 24 hours',
                               img1=session['proimage'])
    except (SMTPAuthenticationError,gaierror) as arg:
        print(arg)
        if str(arg) in 'getaddrinfo failed':
            flash('error')
            return render_template('html/AtmPrgmFiles/home2.html', uname=session['username'],
                                   msg='check your internet connection and try again',img1=session['proimage'])
        else:
            flash('error')
            return render_template('html/AtmPrgmFiles/home2.html', uname=session['username'],
                                   msg='the built-insecurity features in Gmail service may block this login attempt.please '
                                       'login to your gmail and turn on the less secure apps option,if it is done then check your username and password and try again',
                                   img1=session['proimage'])



##################################################################

@app.route('/google')
def f16():
    return render_template('html/AtmPrgmFiles/googlepage.html')

if sess==1:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response

if __name__=="__main__":
    app.run(debug=True)

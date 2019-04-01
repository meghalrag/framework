import requests
from click import DateTime
from flask import Flask, redirect, url_for, render_template, request, session, Response, make_response
from cachecontrol import CacheControl

app1=Flask('')

@app1.route('/es')
def postdataindex1():
    return render_template('html/AtmPrgmFiles/logandsignup.html')

@app1.route('/register',methods=['post','get'])
def postdata():
    fname=request.form['fname']
    lname=request.form['lname']
    uname=request.form['uname']
    passw=request.form['passw']
    cpassw = request.form['cpassw']
    return redirect(url_for('fun4',fname=fname,lname=lname,uname=uname,passw=passw,cpassw=cpassw))
    # return request.form['name']


@app1.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@app1.route('/render/<fname>/<lname>/<uname>/<passw>/<cpassw>')
def fun4(fname,lname,uname,passw,cpassw):
    return render_template('frame.html',fname=fname,lname=lname,uname=uname,passw=passw,cpassw=cpassw)

######session#############

app1.secret_key='skey'
app1.config['SESSION_TYPE']='filesystem'
@app1.route('/index')
def fun6():
    return render_template('html/sessionsample.html')
@app1.route('/session',methods=['post','get'])
def setSession():
    session['username']=request.form['user']

    return render_template('html/home.html',uname=session['username'],username=request.form['user'],password=request.form['pass'])
@app1.route('/logout')
def logout():
    session.pop('username')
    return render_template('html/logout.html')

######session#############

######cookiepgm#############

@app1.route('/cookie/<name>')
def fun1(name):
    res=make_response('ok')
    res.set_cookie('names',name)
    return res
@app1.route('/getcookie')
def fun2():
    value=request.cookies.get('names')
    return render_template('html/logout.html',val=value)


######cookiepgm#############

if __name__=="__main__":
    app1.run(debug=True)
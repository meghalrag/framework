from flask import Flask, redirect, url_for, render_template, request

app=Flask('')

@app.route('/')
def fun1():
    return 'hello'

@app.route('/return/<name>/<age>')
def fun3(name,age):
    return redirect(url_for('fun2', name = name,age=age))
    # return 'i am {},{}'.format(name, age)

@app.route('/<name>/<age>')
def fun2(name,age):
    return 'i am {},{}'.format(name,age)

@app.route('/postdataindex')
def postdataindex():
    return render_template('frame3.html')

@app.route('/postdata',methods=['post','get'])
def postdata():
    name=request.form['name']
    age=request.form['age']
    return redirect(url_for('fun4',name=name,age=age))
    # return request.form['name']


@app.route('/render/<name>/<age>')
def fun4(name,age):
    return render_template('html/frame123.html',name=name,age=age)

if __name__=="__main__":
    app.run(debug=True)
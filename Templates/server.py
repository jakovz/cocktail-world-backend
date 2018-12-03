from flask import Flask, render_template, redirect, url_for, request, make_response,session
import datetime
app = Flask(__name__)



@app.route('/login3', methods=['POST', 'GET'])
def login3():

    if request.method == 'GET':
        if 'is_logged_in' in session:
            if session['is_logged_in'] is True:
                return redirect(url_for('post_login3', name=session['user_name']))
        return render_template('login3.html')

    elif request.method == 'POST':
        user = request.form['name']
        password = request.form['pass']
        if user == 'amit' and password == '1234':
            session['is_logged_in'] = True
            session['user_name'] = user
        else:
            session['is_logged_in'] = False
        return redirect(url_for('post_login3', name=user))
    
    return ''


@app.route('/after_login3/<name>')
def post_login3(name):
    if 'is_logged_in' in session:
        if session['is_logged_in'] is True:
            return 'welcome %s' % session['user_name']

    return 'failedddddddd'






@app.route('/login2', methods=['POST', 'GET'])
def login2():

    if request.method == 'GET':
        return render_template('login2.html')

    elif request.method == 'POST':
        user = request.form['name']
        password = request.form['pass']
        if user == 'amit' and password == '1234':
            is_successful = 'True'
        else:
            is_successful = 'False'
            user = 'fail'
        resp = make_response(redirect(url_for('post_login2', name=user)))
        resp.set_cookie('successful_login', is_successful)
        return resp


@app.route('/after_login2/<name>')
def post_login2(name):
    is_successful = request.cookies.get('successful_login')
    if is_successful == 'True':
        return 'welcome %s' % name
    else:
        return 'failedddddddd'




@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        user = request.form['name']
        password = request.form['pass']
        if user == 'amit' and password == '1234':
            return redirect(url_for('post_login', name=user))
        else:
            return redirect(url_for('post_login', name='fail'))


@app.route('/after_login/<name>')
def post_login(name):
    if name == 'fail':
        return 'failedddddddd'
    else:
        return 'welcome %s' % name





@app.route('/advanced_template')
def advanced_template():
    dict = {'python': 100, 'php': 90, 'ruby': 70}
    return render_template('advanced.html', result=dict)


@app.route('/template')
def use_templates():
    return render_template('template.html', the_day=datetime.datetime.today())


@app.route('/')
def hello_world():
    return "Hello dear DB students!"


if __name__ == '__main__':
    app.secret_key = 'itsasecret'
    app.run(port=8888, host="0.0.0.0", debug=True)








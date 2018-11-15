from flask import Flask, render_template, redirect, request, session, escape, url_for
from classes.pharrell import Pharrell

app = Flask(__name__)

app.secret_key = b'dmVyeXZlcnl2ZXJ5c2VjdXJl'

@app.route('/', methods=['GET'])
@app.route('/<path>', methods=['GET'])
def hello_world(path=''):

    if path == 'redirect':
        return redirect('/youve_been_redirected')

    return render_template('root.html', path=path, message=Pharrell().get_message())

@app.errorhandler(404)
def fourohfour(error):
    return '404!', 404

@app.route('/secure', methods=['GET', 'POST'])
def access_secure_area():
    if 'username' in session:
        return '''
                <h2>Logged in as '{}'</h2>
                <a href="{}">Logout</a>
            '''.format(escape(session['username']), url_for('logout'))
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('access_secure_area'))
    return '''
        <form method="POST">
            <p><input type="text" name="username">
            <p><input type="submit" value="Login">
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('hello_world'))

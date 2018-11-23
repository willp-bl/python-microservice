# -*- coding: utf-8 -*-
from flask import Flask, redirect, request, session, escape, url_for
from flask_assets import Bundle
# overriding the normal jinja2 Environment so it loads the govuk-frontend template.njk
from govuk_frontend.templates import Environment
from jinja2 import select_autoescape

from classes.pharrell import Pharrell

app = Flask(__name__, static_folder='node_modules/govuk-frontend/assets', static_url_path='/assets')

app.secret_key = b'dmVyeXZlcnl2ZXJ5c2VjdXJl'

env = Environment(
    autoescape=select_autoescape(['html', 'xml'])
)

scss = Bundle('all.scss', filters='pyscss', output='all.css')
env.register('scss_all', scss)

@app.route('/', methods=['GET'])
@app.route('/<path>', methods=['GET'])
def hello_world(path=''):

    if path == 'redirect':
        return redirect('/youve_been_redirected')

    template = env.get_template('template.njk')
    return template.render(path=path, message=Pharrell().get_message())

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

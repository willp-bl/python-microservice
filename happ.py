#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import path

from flask import Flask, redirect, request, session, escape, url_for, send_from_directory
from jinja2 import select_autoescape, ChoiceLoader, FileSystemLoader, Environment

from classes.pharrell import Pharrell


# from https://github.com/lfdebrux/govuk-frontend-python/blob/d3dd9f6cb689731753346746d2b5c7229f5293e2/govuk_frontend/templates.py#L12
class Environment2(Environment):
    def join_path(self, template, parent):
        """Enable the use of relative paths in template import statements"""
        return path.normpath(path.join(path.dirname(parent), template))


app = Flask(__name__)
env = Environment2(loader=ChoiceLoader([FileSystemLoader('templates/'), FileSystemLoader("node_modules/govuk-frontend/")]),
                  autoescape=select_autoescape(['html', 'xml']),
                  extensions=[])

app.secret_key = b'dmVyeXZlcnl2ZXJ5c2VjdXJl'

@app.route('/', methods=['GET'])
@app.route('/<path>', methods=['GET'])
def hello_world(path=''):

    if path == 'redirect':
        return redirect('/youve_been_redirected')

    template = env.get_template('index.html')
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

# load assets directly from govuk-frontend package
# this is done instead of overriding the `static` directory in Flask()
@app.route('/assets/<path:filename>')
def send_file(filename):
    return send_from_directory('node_modules/govuk-frontend/assets/', filename)

#if __name__ == '__main__':
#    app.run()

from flask import Flask
from flask import render_template
from flask import redirect

app = Flask(__name__)


@app.route('/', methods=['GET'])
@app.route('/<path>', methods=['GET'])
def hello_world(path=''):

    if path == 'redirect':
        return redirect('/youve_been_redirected')

    return render_template('root.html', path=path)

@app.errorhandler(404)
def fourohfour(error):
    return '404!', 404

from flask import Flask
from flask import url_for
from markupsafe import escape


app = Flask(__name__)


@app.route('/')
#@app.route('/index')
#@app.route('/home')
def hello():
    #return 'Welcome to My Watchlist! 欢迎来到我的 Watchlist!'
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'


@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'

@app.route('/test')
def test_url_for():
    #下面是一些调用示例
    # print(url_for('hello'))

    # print(url_for('user_page', name='greyli'))

    # print(url_for('user_page', name='peter'))

    # print(url_for('test_url_for'))

    print(url_for('test_url_for', num=2))
    return 'Test page'


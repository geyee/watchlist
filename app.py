import os
import sys

import click

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from markupsafe import escape
from flask import request, url_for, redirect, flash


WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)


app.config['SECRET_KEY'] = 'dev'


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    name = 'Grey Li'
    movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model): #表名将是 movie
    id = db.Column(db.Integer, primary_key=True) #主键
    title = db.Column(db.String(60)) #电影标题
    year = db.Column(db.String(4)) #电影年份


@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    return render_template('404.html', user=user), 404


@app.route('/', methods=['GET', 'POST'])
#@app.route('/index')
#@app.route('/home')
def index():
    if request.method == 'POST':
        title= request.form.get("title")
        year=request.form.get('year')

        #验证数据
        if not title or not year or len(year)>4 or len(title)>60:
            flash('Invalid input.')
            return redirect(url_for('index'))
        movie=Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')

    # user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

    # return render_template('index.html',user=user,movies=movies)
# def hello():
#     #return 'Welcome to My Watchlist! 欢迎来到我的 Watchlist!'
#     return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'


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



@app.route('/movie/edit/<int:movie_id>', methods=['GET','POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) !=4 or len(title) >60:
            flash('Invalid input.')
            return redirect('edit', movie_id=movie_id)

        movie.title = title
        movie.year =year
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted. ')
    return redirect(url_for('index'))

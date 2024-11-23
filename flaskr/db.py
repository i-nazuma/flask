# flaskr/db.py
import sqlite3
from flask import current_app, g
import click

def get_db():
    db = getattr(g, '_db', None)
    if db is None:
        db = g._db = sqlite3.connect(current_app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

def init_db():
    """初始化数据库"""
    db = get_db()
    with current_app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@click.command('init-db')
def init_db_command():
    """清空现有的数据并初始化数据库"""
    init_db()
    print('Initialized the database.')

def init_app(app):
    """注册数据库命令"""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def close_db(error):
    """关闭数据库连接"""
    db = getattr(g, '_db', None)
    if db is not None:
        db.close()

def get_user_by_username(username):
    db = get_db()
    return db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

def create_user(username, password):
    db = get_db()
    db.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, password))
    db.commit()

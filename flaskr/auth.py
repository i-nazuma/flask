# flaskr/auth.py
# flaskr/auth.py
import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db, create_user

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db_user = get_db().execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone()
        
        if db_user is not None:
            flash('Username is already taken.')
        else:
            create_user(username, generate_password_hash(password))
            flash('User created successfully.')
            return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_db().execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()

        if user is None or not check_password_hash(user['password'], password):
            flash('Incorrect username or password.')
        else:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
    
    return render_template('login.html')

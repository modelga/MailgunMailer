# -*- coding: utf-8 -*-
from datetime import timedelta

from flask import render_template, request, url_for, session, redirect

from app import app
from app.models.Login import login_required
from app.models.SQL_DB import auth_user, User


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not auth_user(username, password):
            error = 'Invalid credentials. Please try again.'
        else:
            user_data = User.query.filter_by(username=username).first()
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=720)
            session['logged_in'] = True
            session['username'] = username
            session['username_id'] = user_data.id
            session['admin'] = user_data.admin
            session['name_1'] = user_data.name_1
            session['name_2'] = user_data.name_2
            session['gravatar'] = user_data.email_md5
            session['mg_api_private'] = user_data.mg_api_private
            session['mg_domain'] = user_data.mg_domain
            session['mg_sender'] = user_data.mg_sender
            return redirect(url_for('index'))

    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


@app.route('/')
@login_required
def index():
    return redirect(url_for('newsletters_index'))

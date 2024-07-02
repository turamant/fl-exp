from flask import (Blueprint, render_template, redirect,
                   url_for, flash, request, session)
from werkzeug.security import generate_password_hash
from app.models import db, User, Score
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Реализация аутентификации пользователя
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Неправильное имя пользователя или пароль', 'danger')
    
    
    return render_template('auth/login.html')

@auth.route('/logout')
def logout():
    # Реализация выхода пользователя
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Реализация регистрации пользователя
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Пользователь с таким именем уже существует', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        
        flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth.route('/profile', methods=['GET'])
@login_required
def user_profile():
    user = User.query.get(current_user.id)

    if not user:
        return "User not found", 404
    
    scores = Score.query.filter_by(user_id=current_user.id).order_by(Score.date.desc()).all()

    return render_template('auth/profile.html', user=user, scores=scores, username=current_user.username,)

@auth.route('/delete_score/<int:score_id>', methods=['POST'])
@login_required
def delete_score(score_id):
    score = Score.query.get(score_id)

    if not score or score.user_id != current_user.id:
        return "Score not found or unauthorized", 404

    db.session.delete(score)
    db.session.commit()

    return redirect(url_for('auth.user_profile'))
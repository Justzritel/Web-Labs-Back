from flask import Blueprint, render_template, jsonify, request, session, flash, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users
import random
import hashlib
import time

lab9 = Blueprint('lab9', __name__)

users_data = {}

congratulations = [
    "С Новым Годом! Пусть этот год принесет вам море счастья и улыбок!",
    "Желаю здоровья, благополучия и исполнения всех желаний!",
    "Пусть в вашем доме всегда царят мир, любовь и достаток!",
    "Пусть новый год будет полон ярких событий и приятных сюрпризов!",
    "Желаю профессиональных успехов и карьерного роста!",
    "Пусть новый год принесет много радости и тепла!",
    "Желаю крепкого здоровья, семейного счастья и финансового благополучия!",
    "Пусть все мечты сбываются, а планы реализуются в новом году!",
    "Желаю новых интересных знакомств и верных друзей!",
    "Пусть новый год будет лучше предыдущего во всех отношениях!"
]

gift_images = [f"/static/lab9/gifts/gift{i+1}.png" for i in range(10)]
requires_auth = [5, 6, 7, 8, 9]

def get_user_data():
    if 'lab9_user' not in session:
        session['lab9_user'] = hashlib.md5(f"{time.time()}{random.random()}".encode()).hexdigest()[:10]
    
    user_id = session['lab9_user']
    
    if user_id not in users_data:
        users_data[user_id] = {
            'opened_boxes': [],
            'username': current_user.login if current_user.is_authenticated else 'Гость',
            'authenticated': current_user.is_authenticated
        }
    
    # Всегда обновляем статус авторизации
    users_data[user_id]['authenticated'] = current_user.is_authenticated
    if current_user.is_authenticated:
        users_data[user_id]['username'] = current_user.login
    else:
        users_data[user_id]['username'] = 'Гость'
    
    return users_data[user_id]

@lab9.route('/lab9/')
def lab():
    user_data = get_user_data()
    
    boxes = []
    for i in range(10):
        boxes.append({
            'index': i,
            'opened': i in user_data['opened_boxes'],
            'requires_auth': i in requires_auth
        })
    
    opened = len(user_data['opened_boxes'])
    max_boxes = 5 if user_data['authenticated'] else 3
    
    return render_template('lab9/index.html',
                         boxes=boxes,
                         opened_count=opened,
                         max_boxes=max_boxes,
                         is_authenticated=user_data['authenticated'],
                         username=user_data['username'])

@lab9.route('/lab9/open/<int:box_id>')
def open_gift(box_id):
    if box_id < 0 or box_id >= 10:
        flash('Неверный номер подарка', 'error')
        return redirect('/lab9/')
    
    user_data = get_user_data()
    
    # Проверяем авторизацию для премиум подарков
    if box_id in requires_auth and not user_data['authenticated']:
        flash('Этот подарок доступен только авторизованным пользователям. Пожалуйста, войдите в систему!', 'error')
        return redirect('/lab9/')
    
    # Проверяем лимит
    max_boxes = 5 if user_data['authenticated'] else 3
    if len(user_data['opened_boxes']) >= max_boxes:
        flash(f'Вы достигли лимита открытых подарков ({max_boxes})!', 'error')
        return redirect('/lab9/')
    
    # Если коробка уже открыта, просто показываем ее
    if box_id in user_data['opened_boxes']:
        return redirect(f'/lab9/view/{box_id}')
    
    # Открываем коробку
    user_data['opened_boxes'].append(box_id)
    
    return redirect(f'/lab9/view/{box_id}')

@lab9.route('/lab9/view/<int:box_id>')
def view_gift(box_id):
    if box_id < 0 or box_id >= 10:
        flash('Неверный номер подарка', 'error')
        return redirect('/lab9/')
    
    user_data = get_user_data()
    
    if box_id not in user_data['opened_boxes']:
        flash('Вы еще не открыли этот подарк', 'error')
        return redirect('/lab9/')
    
    return render_template('lab9/gift.html',
                         gift_id=box_id,
                         image=gift_images[box_id],
                         message=congratulations[box_id],
                         username=user_data['username'])

@lab9.route('/lab9/santa', methods=['POST'])
@login_required
def santa():
    user_data = get_user_data()
    user_data['opened_boxes'] = []
    return jsonify({'success': True})

@lab9.route('/lab9/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/lab9/')
    
    if request.method == 'GET':
        return render_template('lab9/login.html')
    
    username = request.form.get('username')
    password = request.form.get('password')
    remember = request.form.get('remember')
    
    if not username or not password:
        flash('Введите логин и пароль', 'error')
        return render_template('lab9/login.html')
    
    user = users.query.filter_by(login=username).first()
    
    if not user or not check_password_hash(user.password, password):
        flash('Неверный логин или пароль', 'error')
        return render_template('lab9/login.html')
    
    login_user(user, remember=bool(remember))
    flash('Вы успешно вошли в систему!', 'success')
    return redirect('/lab9/')

@lab9.route('/lab9/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/lab9/')
    
    if request.method == 'GET':
        return render_template('lab9/register.html')
    
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    if not username or not password:
        flash('Введите логин и пароль', 'error')
        return render_template('lab9/register.html')
    
    if password != confirm_password:
        flash('Пароли не совпадают', 'error')
        return render_template('lab9/register.html')
    
    existing_user = users.query.filter_by(login=username).first()
    if existing_user:
        flash('Пользователь с таким логином уже существует', 'error')
        return render_template('lab9/register.html')
    
    try:
        hashed_password = generate_password_hash(password)
        new_user = users(login=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        flash('Регистрация успешна! Добро пожаловать!', 'success')
        return redirect('/lab9/')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при регистрации: {str(e)}', 'error')
        return render_template('lab9/register.html')

@lab9.route('/lab9/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'success')
    return redirect('/lab9/')
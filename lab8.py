from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    username = session.get('username', 'anonymous')
    return render_template('lab8/lab8.html', username=username)

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')


    if not login_form or login_form.strip() == '':
        return render_template('lab8/register.html', 
                               error="Имя пользователя не может быть пустым")

    if not password_form or password_form.strip() == '':
        return render_template('lab8/register.html', 
                               error="Пароль не может быть пустым")


    existing_user = users.query.filter_by(login=login_form).first()
    if existing_user:
        return render_template('lab8/register.html', 
                               error="Пользователь с таким логином уже существует")

    # Хэширование пароля и создание пользователя
    try:
        password_hash = generate_password_hash(password_form)
        new_user = users(login=login_form, password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        
        
        return redirect('/lab8/')
        
    except Exception as e:
        db.session.rollback()
        return render_template('lab8/register.html', 
                               error=f"Ошибка при регистрации: {str(e)}")
    

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    # Проверяем, не авторизован ли пользователь уже
    if current_user.is_authenticated:
        return redirect('/lab8/')
    
    if request.method == 'GET':
        return render_template('lab8/login.html')
    

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    

    if not login_form or login_form.strip() == '':
        return render_template('lab8/login.html', 
                               error="Введите логин")
    
    if not password_form or password_form.strip() == '':
        return render_template('lab8/login.html', 
                               error="Введите пароль")
    
    user = users.query.filter_by(login=login_form).first()
    

    if not user:
        return render_template('lab8/login.html', 
                               error="Пользователь не найден")
    
    if not check_password_hash(user.password, password_form):
        return render_template('lab8/login.html', 
                               error="Неверный пароль")
    
    # УСПЕШНАЯ АУТЕНТИФИКАЦИЯ - вход в систему
    # Используем remember=True если галочка установлена
    login_user(user, remember= False)
    
    flash(f"Добро пожаловать, {user.login}!", "success")
    
    # Перенаправление на главную страницу
    return redirect('/lab8/')    

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    return "Список статей"
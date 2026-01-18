from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    # Используем current_user из Flask-Login
    username = current_user.login if current_user.is_authenticated else 'anonymous'
    return render_template('lab8/lab8.html', username=username)

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    # Проверка на пустое имя пользователя
    if not login_form or login_form.strip() == '':
        return render_template('lab8/register.html', 
                               error="Имя пользователя не может быть пустым")

    # Проверка на пустой пароль
    if not password_form or password_form.strip() == '':
        return render_template('lab8/register.html', 
                               error="Пароль не может быть пустым")

    # Проверка существования пользователя
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
        
        login_user(new_user)
        flash("Регистрация  успешна! Добро пожаловать.", "success")
        
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
    
    # Получаем данные из формы
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = request.form.get('remember_me')  # Галочка "запомнить меня"
    
    # Проверка на пустые значения
    if not login_form or login_form.strip() == '':
        return render_template('lab8/login.html', 
                               error="Введите логин")
    
    if not password_form or password_form.strip() == '':
        return render_template('lab8/login.html', 
                               error="Введите пароль")
    
    # Поиск пользователя в базе данных
    user = users.query.filter_by(login=login_form).first()
    
    # Проверка существования пользователя и пароля
    if not user:
        return render_template('lab8/login.html', 
                               error="Пользователь не найден")
    
    if not check_password_hash(user.password, password_form):
        return render_template('lab8/login.html', 
                               error="Неверный пароль")
    

    login_user(user, remember=(remember_me == 'on'))
    
    flash(f"Добро пожаловать, {user.login}!", "success")
    
    # Перенаправление на главную страницу
    return redirect('/lab8/')

@lab8.route('/lab8/articles/')
@login_required
def my_articles():
    # Получаем статьи текущего пользователя
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    
    # Преобразуем в список для удобства работы в шаблоне
    articles_list = []
    for article in user_articles:
        articles_list.append({
            'id': article.id,
            'title': article.title,
            'article_text': article.article_text,
            'is_favorite': article.is_favorite,
            'is_public': article.is_public,
            'likes': article.likes,
            'login_id': article.login_id
        })
    
    return render_template('lab8/my_articles.html', 
                          articles=articles_list, 
                          username=current_user.login)

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')


@lab8.route('/lab8/articles/create/', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create_article.html')
    

    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()
    is_favorite = request.form.get('is_favorite') == 'on'
    is_public = request.form.get('is_public') == 'on'
    

    if not title:
        return render_template('lab8/create_article.html', 
                               error="Введите заголовок статьи")
    
    if not article_text:
        return render_template('lab8/create_article.html', 
                               error="Введите текст статьи")
    
    if len(title) > 50:
        return render_template('lab8/create_article.html', 
                               error="Заголовок не должен превышать 50 символов")
    
   
    try:
        new_article = articles(
            title=title,
            article_text=article_text,
            is_favorite=is_favorite,
            is_public=is_public,
            likes=0,
            login_id=current_user.id
        )
        
        db.session.add(new_article)
        db.session.commit()
        
        flash(f"Статья '{title}' успешно создана!", "success")
        return redirect('/lab8/articles/')
        
    except Exception as e:
        db.session.rollback()
        return render_template('lab8/create_article.html', 
                               error=f"Ошибка при создании статьи: {str(e)}")
    

@lab8.route('/lab8/articles/<int:article_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):

    article = articles.query.get_or_404(article_id)
    
    if article.login_id != current_user.id:
        flash("У вас нет прав для редактирования этой статьи", "error")
        return redirect('/lab8/articles/')
    
    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)
    

    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()
    is_favorite = request.form.get('is_favorite') == 'on'
    is_public = request.form.get('is_public') == 'on'
    
    # Валидация
    if not title:
        return render_template('lab8/edit_article.html', 
                               article=article,
                               error="Введите заголовок статьи")
    
    if not article_text:
        return render_template('lab8/edit_article.html', 
                               article=article,
                               error="Введите текст статьи")
    

    try:
        article.title = title
        article.article_text = article_text
        article.is_favorite = is_favorite
        article.is_public = is_public
        
        db.session.commit()
        
        flash(f"Статья '{title}' успешно обновлена!", "success")
        return redirect('/lab8/articles/')
        
    except Exception as e:
        db.session.rollback()
        return render_template('lab8/edit_article.html', 
                               article=article,
                               error=f"Ошибка при обновлении статьи: {str(e)}")

@lab8.route('/lab8/articles/<int:article_id>/delete/', methods=['POST'])
@login_required
def delete_article(article_id):
    # Находим статью и проверяем права доступа
    article = articles.query.get_or_404(article_id)
    
    if article.login_id != current_user.id:
        flash("У вас нет прав для удаления этой статьи", "error")
        return redirect('/lab8/articles/')
    
    try:
        title = article.title
        db.session.delete(article)
        db.session.commit()
        
        flash(f"Статья '{title}' успешно удалена!", "success")
        return redirect('/lab8/articles/')
        
    except Exception as e:
        db.session.rollback()
        flash(f"Ошибка при удалении статьи: {str(e)}", "error")
        return redirect('/lab8/articles/')
    
@lab8.route('/lab8/articles/public/')
def public_articles():
    # Получаем публичные статьи вместе с информацией об авторах через join
    public_articles_list = db.session.query(
        articles, users.login
    ).join(
        users, articles.login_id == users.id
    ).filter(
        articles.is_public == True
    ).all()
    
    # Преобразуем результат в удобный формат
    articles_data = []
    for article, author_login in public_articles_list:
        articles_data.append({
            'id': article.id,
            'title': article.title,
            'article_text': article.article_text,
            'is_favorite': article.is_favorite,
            'is_public': article.is_public,
            'likes': article.likes,
            'author': author_login,
            'login_id': article.login_id
        })
    
    return render_template('lab8/public_articles.html', articles=articles_data)

@lab8.route('/lab8/articles/search/', methods=['GET', 'POST'])
def search_articles():
    if request.method == 'GET':
        return render_template('lab8/search.html')
    
    search_query = request.form.get('search_query', '').strip()
    if not search_query:
        return render_template('lab8/search.html', error="Введите поисковый запрос")
    
    try:
        # Используем join для получения информации об авторе
        search_results = db.session.query(
            articles, users.login
        ).join(
            users, articles.login_id == users.id
        ).filter(
            db.or_(
                articles.title.ilike(f'%{search_query}%'),
                articles.article_text.ilike(f'%{search_query}%')
            ),
            articles.is_public == True
        ).all()
        
        # Преобразуем результат в удобный формат
        articles_data = []
        for article, author_login in search_results:
            articles_data.append({
                'id': article.id,
                'title': article.title,
                'article_text': article.article_text,
                'is_favorite': article.is_favorite,
                'is_public': article.is_public,
                'likes': article.likes,
                'author': author_login,
                'login_id': article.login_id
            })
        
        return render_template('lab8/search.html', 
                              articles=articles_data, 
                              search_query=search_query,
                              results_count=len(articles_data))
        
    except Exception as e:
        return render_template('lab8/search.html', 
                              error=f"Ошибка при поиске: {str(e)}")
    


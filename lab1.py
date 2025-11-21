from flask import Blueprint, url_for, redirect,request
import datetime
lab1 = Blueprint('lab1', __name__)

@lab1.route("/lab1")
def lab():
    return """<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>
        <main>
            <h1>Первая лабораторная работа</h1>
            
            <p>Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые ба-
            зовые возможности.</p>
            
            <a href=""" + url_for('index') + """>Вернуться на главную</a>
            
            <h2>Список роутов</h2>
            <ul>
                <li><a href=""" + url_for('lab1.web') + """>Web-сервер</a></li>
                <li><a href=""" + url_for('lab1.author') + """>Об авторе</a></li>
                <li><a href=""" + url_for('lab1.image') + """>Изображение</a></li>
                <li><a href=""" + url_for('lab1.counter') + """>Счетчик посещений</a></li>
                <li><a href=""" + url_for('lab1.info') + """>Перенаправление</a></li>
                <li><a href=""" + url_for('lab1.created') + """>Создание</a></li>
            </ul>
        </main>
        <footer>
            Крадинов Анатолий Иванович, ФБИ-33, 3 курс, 2025
        </footer>
    </body>
</html>"""



@lab1.route("/lab1/web")
def web():
    return '''<!doctype html>
        <html>
            <body>
               <h1>web-сервер на flask</h1>
            </body>
        </html>''', 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }


@lab1.route("/lab1/author")
def author():
    name = "Крадинов Анатолий Иванович"
    group = "ФБИ-33"
    faculty = "ФБ"

    return """<!doctype html>
    <html> 
       <body>
           <p>Студент: """+ name + """<p>
           <p>Группа: """+ group + """<p>
           <p>Факультет: """+ faculty + """<p>
           <a href='/web/>web</a>
        </body>
    </html>"""


@lab1.route("/lab1/image")
def image():
    path = url_for("static", filename="image.jpg")
    css_path = url_for("static", filename="lab1.css")
    html_content="""<!doctype html>
<html> 
    <head>
        <title>Хорошее, а не плохое</title>
        <link rel="stylesheet" href=""" + css_path + """>
    </head>
    <body>
            <div class="container">
                <link rel="stylesheet" href=""" + css_path + """>
                <h1>Делайте хорошее, а плохое не делайте</h1>
                <img src=""" + path + """>
            </div>
        </body>
</html>"""
    return html_content, 200, {
        'Content-Language': 'ru',
        'X-MEM': 'FINE',
        'X-Server-Technology': 'Flask Python Framework',
        'Content-Type': 'text/html; charset=utf-8'
    }


count = 0
@lab1.route("/lab1/counter")
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    return """<!doctype html>
    <html> 
        <body>
            Счетчик посещения страницы """ + str(count) + """
            <hr>
            Дата и время: """ + str(time) + """<br>
            Запрошенный адрес:""" + str(url) + """<br>
            Ваш IP адрес:""" + str(client_ip) + """<br>
            <hr>
            <a href=""" + url_for('lab1.reset_counter') + """>Сбросить счетчик</a>
        </body>
    </html>"""


@lab1.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return redirect(url_for('lab1.counter'))


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/lab1/created")
def created():
    return """<!doctype html>
    <html> 
        <body>
            <h1>Создано успешно</h1>
            <div><i>Создано</i></div>
        </body>
    </html>""", 201



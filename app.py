from flask import Flask, url_for, request, redirect, render_template_string, abort, render_template
import datetime
app= Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return """<!doctype html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
        </header>
        <main>
            <menu>
                <li><a href=""" + url_for('lab1') + """>Первая лабораторная</a></li>
            </menu>
        </main>
        <footer>
            Крадинов Анатолий Иванович, ФБИ-33, 3 курс, 2025
        </footer>
    </body>
    </html>"""

@app.route("/lab1")
def lab1():
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
                <li><a href=""" + url_for('index') + """>Web-сервер</a></li>
                <li><a href=""" + url_for('func') + """>Об авторе</a></li>
                <li><a href=""" + url_for('image') + """>Изображение</a></li>
                <li><a href=""" + url_for('counter') + """>Счетчик посещений</a></li>
                <li><a href=""" + url_for('info') + """>Перенаправление</a></li>
                <li><a href=""" + url_for('created') + """>Создание</a></li>
            </ul>
        </main>
        <footer>
            Крадинов Анатолий Иванович, ФБИ-33, 3 курс, 2025
        </footer>
    </body>
</html>"""

@app.route("/lab1/author")
def func():
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

@app.route("/lab1/image")
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
@app.route("/lab1/counter")
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
            <a href=""" + url_for('reset_counter') + """>Сбросить счетчик</a>
        </body>
    </html>"""

@app.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return redirect(url_for('counter'))

@app.route("/lab1/info")
def info():
    return redirect("/author")

@app.route("/lab1/created")
def created():
    return """<!doctype html>
    <html> 
        <body>
            <h1>Создано успешно</h1>
            <div><i>Создано</i></div>
        </body>
    </html>""", 201

not_found_logs = []

@app.errorhandler(404)
def not_found(err):
    path_for_404 = url_for("static", filename="404.jpeg")
    client_ip = request.remote_addr
    access_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url
    user_agent = request.headers.get('User-Agent', 'Неизвестно')
    
    log_entry = {
        'ip': client_ip,
        'time': access_time,
        'url': requested_url,
        'user_agent': user_agent
    }
    not_found_logs.append(log_entry)
    
    if len(not_found_logs) > 20:
        not_found_logs.pop(0)
    
    log_html = '<h3>История 404 ошибок:</h3><table border="1" style="width: 100%; border-collapse: collapse;">'
    log_html += '<tr><th>Время</th><th>IP-адрес</th><th>Запрошенный URL</th><th>User-Agent</th></tr>'
    
    for entry in reversed(not_found_logs):
        log_html += f'''
        <tr>
            <td style="padding: 5px;">{entry["time"]}</td>
            <td style="padding: 5px;">{entry["ip"]}</td>
            <td style="padding: 5px;">{entry["url"]}</td>
            <td style="padding: 5px; font-size: 12px;">{entry["user_agent"][:50]}...</td>
        </tr>'''
    
    log_html += '</table>'
    
    return f"""
<!doctype html>
<html>
    <head>
        <title>404 - Страница не найдена</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f5f5f5;
            }}
            .container {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            h1 {{ color: #d32f2f; }}
            .info {{ background: #f0f0f0; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            table {{ margin-top: 20px; font-size: 14px; width: 100%; border-collapse: collapse; }}
            th {{ background: #e0e0e0; padding: 10px; text-align: left; }}
            td {{ padding: 8px; border-bottom: 1px solid #ddd; }}
        </style>
    </head>
    <body>
        <img src=""" + path_for_404 + """>
        <div class="container">
            <h1>404 - Страница не найдена</h1>
            
            <div class="info">
                <p><strong>Ваш IP-адрес:</strong>""" + client_ip + """</p>
                <p><strong>Дата и время доступа:</strong> """+access_time+"""</p>
                <p><strong>Запрошенный URL:</strong> """+requested_url+"""</p>
            </div>
            
            <p>К сожалению, запрашиваемая страница не существует.</p>
            <p>Вернитесь на <a href="{url_for('index')}">главную страницу</a> или воспользуйтесь меню навигации.</p>
            
            <p><strong>"""+log_html+"""</p>
        </div>
    </body>
</html>
""", 404

@app.route('/401')
def unauthorized():
    return '''
<!doctype html>
<html>
    <head>
        <title>401 Unauthorized</title>
    </head>
    <body>
        <h1>401 Unauthorized</h1>
        <p>Требуется аутентификация для доступа к ресурсу.</p>
    </body>
</html>
''', 401

@app.route('/402')
def payment_required():
    return '''
<!doctype html>
<html>
    <head>
        <title>402 Payment Required</title>
    </head>
    <body>
        <h1>402 Payment Required</h1>
        <p>Требуется оплата для доступа к ресурсу.</p>
    </body>
</html>
''', 402

@app.route('/403')
def forbidden():
    return '''
<!doctype html>
<html>
    <head>
        <title>403 Forbidden</title>
    </head>
    <body>
        <h1>403 Forbidden</h1>
        <p>Доступ к запрошенному ресурсу запрещен.</p>
    </body>
</html>
''', 403

@app.route('/405')
def method_not_allowed():
    return '''
<!doctype html>
<html>
    <head>
        <title>405 Method Not Allowed</title>
    </head>
    <body>
        <h1>405 Method Not Allowed</h1>
        <p>Метод запроса не поддерживается для данного ресурса.</p>
    </body>
</html>
''', 405

@app.route('/418')
def teapot():
    return '''
<!doctype html>
<html>
    <head>
        <title>418 I'm a teapot</title>
    </head>
    <body>
        <h1>418 I'm a teapot</h1>
        <p>Я чайник и не могу заваривать кофе.</p>
        <p>Это шуточный код ошибки .</p>
    </body>
</html>
''', 418
@app.route('/server_error')
def server_error_test():
    result = 10 / 0
    return "Этот код никогда не выполнится"

@app.errorhandler(500)
def internal_server_error(err):
    return '''
<!doctype html>
<html>
    <head>
        <title>500 - Ошибка сервера</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                min-height: 100vh;
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .error-container {
                background: rgba(255, 255, 255, 0.95);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
                max-width: 600px;
                margin: 20px;
                text-align: center;
                border-left: 6px solid #c23616;
            }
            .error-code {
                font-size: 80px;
                font-weight: 900;
                color: #c23616;
                margin: 0;
                line-height: 1;
            }
            .error-title {
                color: #2f3640;
                font-size: 28px;
                margin: 10px 0 20px 0;
                font-weight: 600;
            }
            .error-description {
                color: #718093;
                font-size: 18px;
                margin-bottom: 30px;
                line-height: 1.5;
            }
            .info-panel {
                background: #f8f9fa;
                padding: 25px;
                border-radius: 12px;
                margin: 25px 0;
                text-align: left;
                border: 1px solid #e9ecef;
            }
            .info-title {
                color: #2f3640;
                font-size: 20px;
                margin-bottom: 15px;
                font-weight: 600;
            }
            .suggestion-list {
                background: #fff;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
                border-left: 4px solid #44bd32;
            }
            .suggestion-list ul {
                text-align: left;
                max-width: 400px;
                margin: 0 auto;
                padding-left: 20px;
            }
            .suggestion-list li {
                margin-bottom: 10px;
                color: #2f3640;
            }
            .tech-details {
                background: #2f3640;
                color: white;
                padding: 25px;
                border-radius: 10px;
                margin: 25px 0;
                text-align: left;
            }
            .tech-title {
                font-size: 20px;
                margin-bottom: 15px;
                font-weight: 600;
                color: #44bd32;
            }
            .tech-details p {
                margin: 12px 0;
                font-family: monospace;
                font-size: 14px;
                line-height: 1.4;
            }
            .home-link {
                color: #44bd32;
                text-decoration: none;
                font-weight: 600;
                font-size: 16px;
            }
            .home-link:hover {
                text-decoration: underline;
            }
            .quote {
                font-style: italic;
                color: #7f8fa6;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px dashed #dcdde1;
                font-size: 16px;
            }
        </style>
    </head>
    <body>
        <div class="error-container">
            <div class="error-code">500</div>
            <h1 class="error-title">Внутренняя ошибка сервера</h1>
            <p class="error-description">На сервере произошла непредвиденная ошибка. Наша команда уже уведомлена и работает над решением</p>
            
            <div class="info-panel">
                <h3 class="info-title">Возможные причины</h3>
                <ul style="text-align: left; max-width: 400px; margin: 0 auto;">
                    <li>Временные технические неполадки</li>
                    <li>Ошибка в программном коде</li>
                    <li>Проблемы с подключением к базам данных</li>
                    <li>Перегрузка сервера запросами</li>
                </ul>
            </div>
            
            <div class="suggestion-list">
                <h3 class="info-title">Рекомендуемые действия</h3>
                <ul>
                    <li>Повторите попытку через несколько минут</li>
                    <li>Вернитесь на <a href="''' + url_for('index') + '''" class="home-link">главную страницу</a></li>
                    <li>Сообщите о проблеме в техническую поддержку</li>
                    <li>Очистите кэш браузера и попробуйте снова</li>
                </ul>
            </div>
            
            <div class="tech-details">
                <h3 class="tech-title">Техническая информация</h3>
                <p><strong>Тип ошибки:</strong> ''' + str(type(err).__name__) + '''</p>
                <p><strong>Сообщение:</strong> ''' + str(err) + '''</p>
                <p><strong>Код ошибки:</strong> 500 Internal Server Error</p>
            </div>
            
            <div class="quote">
                <p>"Совершенство достигается не тогда, когда нечего добавить, а когда нечего убрать"</p>
            </div>
        </div>
    </body>
</html>
''', 500

@app.route('/lab2/a')
def a():
    return 'без слэша'
@app.route("/lab2/a/")
def a2():
    return 'со слэшем'


flower_list = ['роза','тюльпан','незабудка','ромашка']
@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id > len(flower_list):
        abort(404)
    else:
        return "id=" + flower_list[flower_id]
@app.route('/lab2/flowers/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен цветок</h1>
    <p>Название нового цветка: {name}</p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный список: {flower_list}</p>
    </body>
</html>
'''
@app.route('/lab2/example')
def example():
    name = 'Горшков Андрей'
    nomer = '2'
    group = 'ФБИ-33'
    kurs = '3 курс'
    lab_num = '2'
    fruits = [{'name': 'яблоки', 'price': 100}, 
              {'name': 'груши', 'price': 100}, 
              {'name': 'апельсины' , 'price': 100},
              {'name': 'мандарины', 'price': 100}, 
              {'name': 'манго', 'price': 100},]
    return render_template('example.html', name=name, nomer=nomer, kurs=kurs, group=group, lab_num=lab_num, fruits=fruits)
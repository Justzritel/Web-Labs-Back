from flask import Flask, url_for, request, redirect
import datetime
app= Flask(__name__)

@app.route("/")
@app.route("/lab1/web")
def start():
    return """<!doctype html>
    <html> 
       <body>
           <h1>web-сервер</h1> 
               </html>""", 200, {
                   "X-Server": "sample",
                   "Content-Type": "text/plain; charset=utf-8"
               }

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
    return """<!doctype html>
    <html> 
        <body>
            <link rel="stylesheet" href=""" + css_path + """>
            <h1>Делайте хорошее, а плохое не делайте</h1>
            <img src=""" + path + """>
        </body>
    </html>"""

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

@app.errorhandler(404)
def not_found(err):
    return "Страница не найдена", 404

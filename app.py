from flask import Flask, url_for, request, redirect
import datetime
app= Flask(__name__)

@app.route("/")
@app.route("/web")
def start():
    return """<!doctype html>
    <html> 
       <body>
           <h1>web-сервер</h1> 
               </html>"""

@app.route("/author")
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

@app.route("/image")
def image():
    path = url_for("static", filename="image.jpg")
    return """<!doctype html>
    <html> 
        <body>
            <h1>Делайте хорошее, а плохое не делайте</h1>
            <img src=""" + path + """>
        </body>
    </html>"""

count = 0
@app.route("/counter")
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
        </body>
    </html>"""

@app.route("/info")
def info():
    return redirect("/author")
from flask import Blueprint, url_for, redirect,request,render_template,abort
import datetime
lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/a')
def a():
    return 'без слэша'
@lab2.route("/lab2/a/")
def a2():
    return 'со слэшем'



@lab2.route('/lab2/example')
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

@lab2.route('/lab2/')
def lab_sec():
    return render_template('lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "0 сколько нам открытий чудных..."
    return render_template('filters.html', phrase=phrase)

flowers = [
    {"name": "Роза", "price": 150},
    {"name": "Тюльпан", "price": 90},
    {"name": "Незабудка", "price": 120},
    {"name": "Ромашка", "price": 80}
]

@lab2.route('/lab2/flowers')
def show_flowers():
    return render_template('flowers.html', flowers=flowers)


@lab2.route('/lab2/flowers/add', methods=['POST'])
def add_flower():
    name = request.form.get('name')
    price = request.form.get('price')

    if not name:
        return "Вы не задали имя цветка", 400
    if not price or not price.isdigit():
        return "Цена должна быть числом", 400

    flowers.append({"name": name, "price": int(price)})
    return redirect(url_for('lab2.show_flowers'))

@lab2.route('/lab2/flowers/delete/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flowers):
        abort(404)
    else:
        flowers.pop(flower_id)
        return redirect(url_for('lab2.show_flowers'))

@lab2.route('/lab2/flowers/clear')
def clear_flowers():
    flowers.clear()
    return redirect(url_for('lab2.show_flowers'))


@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@lab2.route('/lab2/calc/<int:a>')
def calc_one_arg(a):
    return redirect(f'/lab2/calc/{a}/1')

@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    if b == 0:
        div_result = "Ошибка: деление на ноль"
    else:
        div_result = a / b

    return f'''
<!doctype html>
<html>
    <head>
        <style>
            .operation {{
                font-size: 18px;
                margin: 5px 0;
            }}
            .result {{
                font-weight: bold;
                color: #2c3e50;
            }}
            .error {{
                color: #e74c3c;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <h1>Калькулятор</h1>
        <p>Первое число: <strong>{a}</strong></p>
        <p>Второе число: <strong>{b}</strong></p>
        <div class="operation">{a} + {b} = <span class="result">{a + b}</span></div>
        <div class="operation">{a} - {b} = <span class="result">{a - b}</span></div>
        <div class="operation">{a} × {b} = <span class="result">{a * b}</span></div>
        <div class="operation">{a} ÷ {b} = <span class="result">{div_result if isinstance(div_result, str) else f"{div_result:.2f}"}</span></div>
        <div class="operation">{a}<sup>{b}</sup> = <span class="result">{a ** b}</span></div>
        <p><a href="/lab2/calc/">Попробовать снова с 1 и 1</a></p>
    </body>
</html>
'''

books = [
    {"author": "Фёдор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 640},
    {"author": "Лев Толстой", "title": "Война и мир", "genre": "Роман-эпопея", "pages": 1225},
    {"author": "Александр Пушкин", "title": "Евгений Онегин", "genre": "Роман в стихах", "pages": 320},
    {'title': 'Три товарища', 'author': 'Ремарк Э.М.', 'genre': 'Роман', 'pages': 480},
    {"author": "Иван Тургенев", "title": "Отцы и дети", "genre": "Роман", "pages": 370},
    {"author": "Николай Гоголь", "title": "Мёртвые души", "genre": "Сатира", "pages": 420},
    {'title': 'Мартин Иден', 'author': 'Лондон Дж.', 'genre': 'Роман', 'pages': 448},
    {'title': 'Братья Карамазовы', 'author': 'Достоевский Ф.М.', 'genre': 'Роман', 'pages': 824},
    {'title': 'Мастер и Маргарита', 'author': 'Булгаков М.А.', 'genre': 'Роман', 'pages': 350},
    {'title': 'Властелин колец', 'author': 'Толкин Дж.Р.Р.', 'genre': 'Фэнтези', 'pages': 1200}
]

@lab2.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)

cat = [
        {"name": "Мейн-кун", "img": "Cats/cat.maine_coon.jpg", "desc": "Крупная порода с дружелюбным характером и кисточками на ушах."},
        {"name": "Сиамская", "img": "Cats/cat.siamese.jpg", "desc": "Элегантная кошка с голубыми глазами и контрастным окрасом."},
        {"name": "Британская короткошерстная", "img": "Cats/cat.british.jpg", "desc": "Плюшевая кошка с круглыми щеками и спокойным нравом."},
        {"name": "Сфинкс", "img": "Cats/cat.sphynx.jpg", "desc": "Бесшерстная порода, известная своей необычной внешностью и теплолюбивостью."},
        {"name": "Персидская", "img": "Cats/cat.persian.jpg", "desc": "Длинношерстная кошка с приплюснутой мордочкой и спокойным характером."},
        {"name": "Бенгальская", "img": "Cats/cat.bengal.jpg", "desc": "Порода с леопардовым окрасом, активная и игривая."},
        {"name": "Русская голубая", "img": "Cats/cat.russian_blue.jpg", "desc": "Кошка с серебристо-голубой шерстью и изумрудными глазами."},
        {"name": "Норвежская лесная", "img": "Cats/cat.norwegian_forest.jpg", "desc": "Крупная пушистая кошка, приспособленная к холодному климату."},
        {"name": "Шотландская вислоухая", "img": "Cats/cat.scottish_fold.jpg", "desc": "Порода с загнутыми вперед ушами и круглыми глазами."},
        {"name": "Абиссинская", "img": "Cats/cat.abyssinian.jpg", "desc": "Стройная кошка с тикированной шерстью и активным темпераментом."}
]

@lab2.route('/lab2/cat')
def show_cat():
    return render_template('cat.html', cats=cat)
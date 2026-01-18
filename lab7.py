from flask import Blueprint, render_template, request, jsonify

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def lab():
    return render_template('lab7/index.html')
films = [
    {
        "title": "The Matrix",
        "title_ru": "Матрица",
        "year": 1999,
        "description": "Хакер по имени Нео узнает, что реальный мир - это иллюзия, созданная машинами, и присоединяется к повстанцам, чтобы сражаться за свободу человечества."
    },
    {
        "title": "Inception",
        "title_ru": "Начало",
        "year": 2010,
        "description": "Профессиональный вор, специализирующийся на краже идей из подсознания, получает задание внедрить идею в сознание человека, что приводит к неожиданным последствиям."
    },
    {
        "title": "Interstellar",
        "title_ru": "Интерстеллар",
        "year": 2014,
        "description": "Группа исследователей использует недавно обнаруженный червоточину, чтобы обойти ограничения космических путешествий и спасти человечество."
    },
    {
        "title": "The Dark Knight",
        "title_ru": "Темный рыцарь",
        "year": 2008,
        "description": "Бэтмен вместе с комиссаром Гордоном и прокурором Харви Дентом борются с хаосом, который сеет в Готэме криминальный гений по кличке Джокер."
    },
    {
        "title": "Parasite",
        "title_ru": "Паразиты",
        "year": 2019,
        "description": "Бедная семья внедряется в жизнь богатого клана, выдавая себя за высококвалифицированных специалистов, что приводит к непредсказуемым последствиям."
    },
    {
        "title": "Fight Club",
        "title_ru": "Бойцовский клуб",
        "year": 1999,
        "description": "Страдающий бессонницей офисный работник и загадочный торговец мылом создают подпольную организацию, которая превращается во что-то большее."
    },
    {
        "title": "The Grand Budapest Hotel",
        "title_ru": "Отель «Гранд Будапешт»",
        "year": 2014,
        "description": "История о консьерже знаменитого европейского отеля между мировыми войнами и о краже бесценной картины эпохи Возрождения."
    },
    {
        "title": "Blade Runner 2049",
        "title_ru": "Бегущий по лезвию 2049",
        "year": 2017,
        "description": "Молодой репликант-«бегущий по лезвию» раскрывает давно похороненную тайну, которая может погрузить общество в хаос."
    },
    {
        "title": "Mad Max: Fury Road",
        "title_ru": "Безумный Макс: Дорога ярости",
        "year": 2015,
        "description": "В постапокалиптической пустыне Макс помогает группе женщин, бегущих от тирана, в эпическом преследовании через пустоши."
    },
    {
        "title": "Everything Everywhere All at Once",
        "title_ru": "Всё везде и сразу",
        "year": 2022,
        "description": "Пожилая китаянка оказывается втянутой в безумное приключение через параллельные вселенные, где только она может спасти мир."
    }
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        return '', 404

    return films[id]

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):

    if id < 0 or id >= len(films):
        return '', 404
    
    del films[id]
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()
    if film['description'] == '':
        return {'description': 'Заполните описание'}, 400
    films[id] = film
    return films[id]

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    data = request.get_json()
    
    if not data:
        return '', 400
    
    required_fields = ['title', 'title_ru', 'year', 'description']
    for field in required_fields:
        if field not in data:
            return f'Missing required field: {field}', 400
    
    new_film = {
        'title': data['title'],
        'title_ru': data['title_ru'],
        'year': data['year'],
        'description': data['description']
    }
    
    films.append(new_film)
    return str(len(films) - 1), 201

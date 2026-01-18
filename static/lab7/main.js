function fillFilmList() {
    fetch('/lab7/rest-api/films/')
    .then(function (data) {
        return data.json();
    })
    .then(function (films) {
        let tbody = document.getElementById('film-list');
        tbody.innerHTML = '';
        
        for(let i = 0; i < films.length; i++) {
            let tr = document.createElement('tr');
            let tdTitleRus = document.createElement('td'); 
            let tdTitle = document.createElement('td');    
            let tdYear = document.createElement('td');
            let tdActions = document.createElement('td');
            
            tdTitleRus.innerText = films[i].title_ru;
            
            // Английское название (второстепенное)
            if (films[i].title) {
                let span = document.createElement('span');
                span.className = 'original-name';
                span.innerText = `(${films[i].title})`;  // Добавляем скобки
                tdTitle.appendChild(span);
            }
            
        
            tdYear.innerText = films[i].year;
            
            // Создаем кнопки
            let editButton = document.createElement('button');
            editButton.innerText = 'редактировать';
            editButton.onclick = function() {
                editFilm(i);
            };
            
            let delButton = document.createElement('button');
            delButton.innerText = 'удалить';
            delButton.onclick = function() {
                deleteFilm(i, films[i].title_ru);
            };
            
            // Добавляем кнопки в ячейку действий
            tdActions.appendChild(editButton);
            tdActions.appendChild(delButton);
            
            // Добавляем ячейки в строку в правильном порядке
            tr.append(tdTitle);     // 1. Оригинальное название
            tr.append(tdTitleRus);  // 2. Русское название
            tr.append(tdYear);      // 3. Год
            tr.append(tdActions);   // 4. Действия
            
            tbody.append(tr);
        }
    })
    .catch(function(error) {
        console.error('Ошибка:', error);
    });
}

// Функция удаления фильма
function deleteFilm(id, title) {
    if(!confirm(`Вы уверены, что хотите удалить фильм "${title}"?`))
        return;
    
    fetch(`/lab7/rest-api/films/${id}`, {method: 'DELETE'})
    .then(function() {
        fillFilmList();
    })
    .catch(function(error) {
        console.error('Ошибка при удалении:', error);
    });
}

// Показываем модальное окно для добавления нового фильма
function addFilm() {
    // Очищаем все поля
    document.getElementById('id').value = '';
    document.getElementById('title_ru').value = '';
    document.getElementById('title').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    
    // Очищаем все ошибки
    document.querySelectorAll('.error').forEach(el => el.innerText = '');
    
    document.querySelector('.modal').style.display = 'block';
}

function editFilm(id) {

    document.querySelectorAll('.error').forEach(el => el.innerText = '');
    
    // Загружаем данные фильма с сервера
    fetch(`/lab7/rest-api/films/${id}`)
    .then(response => response.json())
    .then(film => {
        document.getElementById('id').value = id;
        document.getElementById('title_ru').value = film.title_ru;
        document.getElementById('title').value = film.title;
        document.getElementById('year').value = film.year;
        document.getElementById('description').value = film.description;
        
        document.querySelector('.modal').style.display = 'block';
    })
    .catch(error => {
        console.error('Ошибка при загрузке фильма:', error);
        alert('Ошибка при загрузке данных фильма');
    });
}

// Отправка данных фильма (добавление или редактирование)
function sendFilm() {
    const id = document.getElementById('id').value;
    const title_ru = document.getElementById('title_ru').value;
    const title = document.getElementById('title').value;
    const year = document.getElementById('year').value;
    const description = document.getElementById('description').value;
    
    // Очищаем все ошибки
    document.querySelectorAll('.error').forEach(el => el.innerText = '');
    
    // Проверка обязательных полей
    if (!title_ru.trim() || !year.trim() || !description.trim()) {
        alert('Пожалуйста, заполните все обязательные поля');
        return;
    }
    
    const filmData = {
        title_ru: title_ru,
        title: title || title_ru, // Если оригинальное название пустое, используем русское
        year: parseInt(year),
        description: description
    };
    
    let url = '/lab7/rest-api/films/';
    let method = 'POST';
    
    // Если есть ID, то редактируем существующий фильм
    if (id !== '') {
        url = `/lab7/rest-api/films/${id}`;
        method = 'PUT';
    }
    
    fetch(url, {
        method: method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(filmData)
    })
    .then(function(resp){  
        if(resp.ok){  
            fillFilmList();  
            cancel();
            return {};  
        }  
        return resp.json();  
    })  
    .then(function(errors){  
        if(errors) {
            // Показываем все ошибки
            for(const field in errors) {
                const errorElement = document.getElementById(field + '_error');
                if(errorElement) {
                    errorElement.innerText = errors[field];  
                }
            }
        }
    })
    .catch(function(error) {
        console.error('Ошибка:', error);
        alert('Ошибка при сохранении фильма');
    });
}

// Закрытие модального окна
function cancel() {
    document.querySelector('.modal').style.display = 'none';
    // Очищаем все ошибки
    document.querySelectorAll('.error').forEach(el => el.innerText = '');
}

const style = document.createElement('style');
style.textContent = `
    /* Таблица - космический минимализм */
    table {
        width: 100%;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-collapse: collapse;
        margin: 30px 0;
        font-family: 'SF Pro Text', -apple-system, BlinkMacSystemFont, sans-serif;
        background: rgba(10, 12, 16, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    th {
        background: linear-gradient(135deg, rgba(20, 85, 255, 0.15), rgba(0, 200, 255, 0.1));
        color: #e0f2ff;
        padding: 18px 20px;
        text-align: left;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        font-weight: 600;
        font-size: 15px;
        letter-spacing: 0.3px;
        text-transform: uppercase;
        position: relative;
    }
    
    th::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 20px;
        right: 20px;
        height: 1px;
        background: linear-gradient(90deg, 
            rgba(20, 85, 255, 0.8), 
            rgba(0, 200, 255, 0.8), 
            rgba(20, 85, 255, 0.8));
        opacity: 0.5;
    }
    
    td {
        padding: 16px 20px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
        color: #b0c4d9;
        font-size: 14.5px;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    tr {
        transition: background 0.25s ease;
    }
    
    tr:hover {
        background: rgba(30, 100, 255, 0.03);
    }
    
    tr:hover td {
        color: #e0f2ff;
    }
    
    tr:last-child td {
        border-bottom: none;
    }
    
    /* Кнопки - неоновые с градиентами */
    button {
        padding: 10px 20px;
        margin: 4px 6px 4px 0;
        background: linear-gradient(135deg, #1a2b6d, #1455ff);
        color: white;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        font-size: 13.5px;
        font-weight: 600;
        letter-spacing: 0.2px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 4px 15px rgba(20, 85, 255, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.1), 
            transparent);
        transition: left 0.6s ease;
    }
    
    button:hover::before {
        left: 100%;
    }
    
    button:hover {
        transform: translateY(-2px);
        background: linear-gradient(135deg, #1455ff, #00c8ff);
        box-shadow: 
            0 6px 25px rgba(20, 85, 255, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    button:active {
        transform: translateY(0);
        transition: transform 0.1s;
    }
    
    /* Кнопка добавления - особый стиль */
    button[onclick="addFilm()"] {
        background: linear-gradient(135deg, #00a86b, #00ff95);
        padding: 14px 28px;
        font-size: 15px;
        font-weight: 700;
        border-radius: 12px;
        margin: 10px 0 20px;
        box-shadow: 
            0 6px 20px rgba(0, 168, 107, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.25);
    }
    
    button[onclick="addFilm()"]:hover {
        background: linear-gradient(135deg, #00ff95, #00a86b);
        box-shadow: 
            0 8px 30px rgba(0, 168, 107, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.35);
    }
    
    /* Кнопки действий в таблице */
    button:not([onclick="addFilm()"]) {
        min-width: 100px;
        font-weight: 600;
        border-radius: 8px;
        padding: 9px 16px;
    }
    
    /* Кнопка редактирования */
    button[onclick^="editFilm"] {
        background: linear-gradient(135deg, #8a4db6, #c77dff);
        box-shadow: 
            0 4px 15px rgba(138, 77, 182, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    
    button[onclick^="editFilm"]:hover {
        background: linear-gradient(135deg, #c77dff, #8a4db6);
        box-shadow: 
            0 6px 20px rgba(138, 77, 182, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.25);
    }
    
    /* Кнопка удаления - красный градиент */
    button[onclick^="deleteFilm"] {
        background: linear-gradient(135deg, #b02a2a, #ff4d4d);
        box-shadow: 
            0 4px 15px rgba(176, 42, 42, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    
    button[onclick^="deleteFilm"]:hover {
        background: linear-gradient(135deg, #ff4d4d, #b02a2a);
        box-shadow: 
            0 6px 20px rgba(176, 42, 42, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.25);
    }
    
    /* Модальное окно - стеклянный эффект */
    .modal {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 5, 15, 0.85);
        backdrop-filter: blur(8px);
        z-index: 10000;
        animation: modalFadeIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    @keyframes modalFadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .modal > div {
        background: linear-gradient(135deg, 
            rgba(20, 30, 48, 0.95), 
            rgba(15, 22, 36, 0.98));
        width: 500px;
        margin: 80px auto;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 
            0 25px 50px rgba(0, 0, 0, 0.5),
            0 0 0 1px rgba(255, 255, 255, 0.05),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.07);
        position: relative;
        overflow: hidden;
    }
    
    .modal > div::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(20, 85, 255, 0.5), 
            transparent);
    }
    
    .modal h2 {
        margin: 0 0 25px 0;
        color: #e0f2ff;
        font-size: 24px;
        font-weight: 700;
        text-align: center;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        position: relative;
    }
    
    .modal h2::after {
        content: '';
        position: absolute;
        bottom: -1px;
        left: 30%;
        right: 30%;
        height: 2px;
        background: linear-gradient(90deg, 
            transparent, 
            #1455ff, 
            transparent);
    }
    
    .modal label {
        display: block;
        margin: 18px 0 8px;
        font-weight: 600;
        color: #a0c8ff;
        font-size: 14px;
        letter-spacing: 0.2px;
    }
    
    .modal input, .modal textarea {
        width: 100%;
        padding: 14px 16px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        font-size: 15px;
        box-sizing: border-box;
        color: #e0f2ff;
        font-family: 'SF Pro Text', -apple-system, sans-serif;
        transition: all 0.25s ease;
    }
    
    .modal input:focus, .modal textarea:focus {
        border-color: rgba(20, 85, 255, 0.8);
        background: rgba(20, 85, 255, 0.05);
        outline: none;
        box-shadow: 
            0 0 0 3px rgba(20, 85, 255, 0.15),
            inset 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    .modal textarea {
        min-height: 120px;
        resize: vertical;
        line-height: 1.5;
    }
    
    .modal-buttons {
        margin-top: 30px;
        text-align: right;
        display: flex;
        justify-content: flex-end;
        gap: 12px;
    }
    
    .modal-buttons button {
        min-width: 100px;
        margin: 0;
        font-weight: 600;
        border-radius: 10px;
    }
    
    .modal-buttons button:first-child {
        background: linear-gradient(135deg, #00a86b, #00ff95);
        box-shadow: 
            0 4px 15px rgba(0, 168, 107, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    .modal-buttons button:first-child:hover {
        background: linear-gradient(135deg, #00ff95, #00a86b);
        box-shadow: 
            0 6px 20px rgba(0, 168, 107, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    .modal-buttons button:last-child {
        background: linear-gradient(135deg, #6c757d, #9ba4ab);
        box-shadow: 
            0 4px 15px rgba(108, 117, 125, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    
    .modal-buttons button:last-child:hover {
        background: linear-gradient(135deg, #9ba4ab, #6c757d);
        box-shadow: 
            0 6px 20px rgba(108, 117, 125, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.25);
    }
    
    /* Оригинальное название */
    .original-name {
        font-style: italic;
        color: #00ff95;
        font-size: 0.85em;
        letter-spacing: 0.1px;
        opacity: 0.9;
        display: block;
        margin-top: 3px;
    }
    
    /* Ошибки */
    .error {
        color: #ff6b6b;
        font-size: 12.5px;
        margin-top: 5px;
        font-weight: 500;
        padding-left: 5px;
        letter-spacing: 0.1px;
    }
    
    /* Обязательные поля */
    .required::after {
        content: " *";
        color: #ff6b6b;
        font-weight: 700;
    }
    
    /* Общие стили для страницы */
    body {
        background: linear-gradient(135deg, #0a0c10, #141822);
        color: #e0f2ff;
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        margin: 0;
        padding: 20px;
        min-height: 100vh;
    }
    
    h1 {
        color: #e0f2ff;
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 10px;
        letter-spacing: -0.5px;
    }
    
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }

`;
document.head.appendChild(style);

document.addEventListener('DOMContentLoaded', function() {
    fillFilmList();
});
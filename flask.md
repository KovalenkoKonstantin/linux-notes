# 🧰 1: Установим Flask

**1. Проверь права на каталог /var/www/:**

```bash
ls -ld /var/www/
```
**2. Убедись, что твой пользователь (rootubn) имеет права на запись в этот каталог. Если нет, измени владельца на себя:**

```bash
sudo chown -R $USER:$USER /var/www/
```

**3. Установи python3-venv (если не установлен):**
```bash
sudo apt update -y
sudo apt install -y python3-venv
```

**4. Создай виртуальную среду:**
Перейди в директорию, где находится твой проект (например, `/var/www/`), и создавай виртуальную среду:
```bash
sudo python3 -m venv venv
```
Это создаст папку `venv` в текущей директории, в которой будет изолированная среда Python.

**5. Активируй виртуальную среду:**
```bash
source venv/bin/activate
```
Ты увидишь, что имя виртуальной среды появится в начале строки (`venv`), что будет означать, что виртуальная среда активирована.
Если ты хочешь точно увидеть, в какой директории находится виртуальная среда, можешь использовать команду:
```bash
which python
```
или
```bash
which pip
```
**6. Изменение прав доступа на виртуальную среду**

```bash
sudo chown -R $USER:$USER /var/www/venv
```

**7. Установи Flask в виртуальной среде:**
Теперь, когда виртуальная среда активирована, ты можешь установить Flask:

```bash
pip install flask
```

**8. Проверка:**
Ты можешь проверить, что Flask установлен, запустив команду:

```bash
pip list | sort
```
Ты увидишь, что в списке установленных пакетов есть Flask.

```(venv) rootubn@rootubn-VirtualBox:/var/www$ pip list
Package      Version
------------ -------
blinker      1.9.0
click        8.1.8
Flask        3.1.0
itsdangerous 2.2.0
Jinja2       3.1.6
MarkupSafe   3.0.2
pip          24.0
Werkzeug     3.1.3
```

# 2: Создайте структуру проекта
Давайте создадим папки и файлы для нашего проекта. Структура будет следующей:

```
/www    
    /.vscode
        settings.json
    /local.work                 <--- Основная директория сайта
        /__pycache__            <--- Какой-то кеш
        /cache                  <--- Кэширование
            redis_cache.py      <--- кэширования Redis пока не настроен
        /bin                    <--- мусор
            app_copy.py         <--- созданная когда-то резервная копия приложения
            decode_input_data.py
            extensions.py       <--- Инициализация RedisCache пока не подключено
        /cache
            copy_registry.json
            redis_cache.py      <--- не подключено
        /core
            /__pycache__        <--- Какой-то кеш
            data.py             <--- Пути к файлам
            db.py               <--- Функции работы с SQLite
            predefined_users.py <--- Пользователи по умолчанию
            utils.py            <--- Общие функции (форматирование дат и чисел)
        /data
            employee.json       <--- Файл м данными по сотрудникам
            local.db            <--- База данныз SQLite
            registry.json       <--- Файл с реестром записей           
        /email_service
            /email_service
                __init__.py
                celery_app.py       <--- celery_app + конфиг
                events.py           <--- Логика уведомлений (реальные функции)
                mailer.py           <--- Функция send_email
                tasks.py            <--- задачи Celery. Обёртки задач над events
                /tests
                    __init__.py
                    test_events.py
                    test_mailer.py
            .env                <--- переменные окружения
            docker-compose.yml
            Dockerfile
            Makefile
            pyproject.toml
            requirements.txt
        /fapi_service
            /routes
            /static
            /templates
            /venv
            __init__.py
            .gitignore
            fastapi_app.py
            requirements.txt
            setup.py
            test_notify.py
        /images
            background.png          <--- Картинки фона
            background2.png         <--- Картинки фона
        /project_service
            /manual_tests                      <--- ручные тесты. не замоканные
                test_celery_config.py           <--- проверка конфигурации Celery + отправка письма
                test_dump_env.py                <--- дамп переменных пярмо в консоль
                test_email_worker.py            <--- реальная отправка письма
                test_service.py                 <--- статус systemd сервиса
                test_tasks.py                   <--- проверка вызова задач
            /media
            /project_lifecycle
                /management
                    /commands                   <--- Django найдёт команду только если она лежит в management/commands/
                        ensure_celerybeat.py    <--- Команда, которая создаёт/обновляет расписание в django-celery-beat
                /migrations
                /templates
                    dashboard.html
                    project_form.html
                __init__.py             <--- пустой
                admin.py
                apps.py
                asgi.py
                celery_app.py           <--- ищет этапы с наступившим transition_to_fixed_at
                models.py               <--- Модели Project и Stages
                settings.py             <--- Главный файл настроек
                tasks.py                <--- планировщик, который находит актуальные этапы и вызывает по имени таск из email_service
                urls.py
                views.py                <--- главная логика
                wsgi.py
            /static
                autosize_textarea.js
                dashboard.css
                dashboard.js
            /staticfiles
            .env
            .gitingore
            db.sqlite3
            Makefile
            manage.py                   <--- Точка входа
            poetry.lock
            pyproject.toml
            README.md
        /routes                 <--- Маршруты Flask
            /__pycache__        <--- Какой-то кеш
            /utils
                celery_client.py<--- Вызовы Celery-задач
            admin.py            <--- Всё, что касается @admin.route
            api.py              <--- @api.route /check_employee
            auth.py             <--- Авторизация, проерка пользователя в БД, logout
            employee_changes.py <--- Маршрут Fast API
            input.py            <--- Всё про форму ввода данных
            main.py             <--- Главная страница, input, preview, registry
            preview_all.py      <--- Маршруты общего просмотра
            registration.py     <--- Процесс регистрации пользователей
            registry.py         <--- Работа с реестром записей
            vhi.py              <--- Маршрут Fast API
            worktime.py         <--- Маршрут Fast API
        /scripts                <--- вспомогательные скрипты
            /__pycache__        <--- Какой-то кеш
            add_total_expenses_per_person_to_db.py
            db_registry_to_json.py
            employee_json_to_db.py
            mssql_db_employee_to_json.py
            registry_json_to_db.py
            sync_json_to_db.py
        /services                   <--- софт линки сами сервисы в /etc/systemd/system/
            email-worker.service    <--- рассылает письма
            project-beat.service    <--- ставит периодику (09:00)
            project-worker.service  <--- выполняет «тик»-таску (читает БД Django)
        /settings
            code.backup.service     <--- Ссылка на сервис автобэкапа кода
            gunicorn.service        <--- Ссылка на настрйоки сервиса гуникорна
            local.work              <--- Жёсткая ссылка на /etc/nginx/sites-available/local.work
            local.work.conf         <--- Жёсткая ссылка на /var/www/local.work/settings/local.work
            nginx.conf              <--- Жёсткая ссылка на /etc/nginx/nginx.conf
        /shared
            Представительские.xlsb  <--- Файл доступный для скачивания всем
        /static
            /css
                act.css
                auth.css
                dashboard.scc
                input.css
                preview_all.css
                print_form.css
                registration.css
                registry.css
                report.css
                start_page.css
            /ico
                ico.ico
            /js
                dashboard.js
                input.js
                print_form.js
                registration.js
                registry.js                
        /tasks                  <-- таски celery пока не настроен
            /__pycache__        <--- Какой-то кеш
            celery_tasks.py     <-- не настроен
        /tasks                          <-- Celery задачи
            celery_tasks.py             <-- Фоновые задачи
        /templates                      <-- шаблоны страниц
            act.html
            dashboard.html
            index.html
            input.html
            login.html
            preview_all.html
            preview_record.html
            print_form.html
            registration.html
            registry.html
            report.html
        /test                               <-- тестовые функции
            /functional
            /integration
                /routes
                    test_admin.py
                    test_api.py
                    test_auth.py
                    test_input.py
                    test_mailer_mocked.py
                    test_mailer_real_send.py
                    test_main.py
                    test_predefined_users.py
                    test_registration.py
                /scripts
            /unit
                /core
                    test_add_total_expenses_per_person_to_db.py
                    test_db_registry_to_json.py
                    test_db.py
                    test_employee_json_to_db.py
                    test_events.py
                    test_mailer.py
                    test_mssql_db_employee_to_json.py
                    test_registry_json_to_db.py
                    test_sync_employee.py
                /utils
                    test_utils.py
            conftest.py
        .coverage
        .goveragerc
        .dockerignore
        .env
        .gitignore
        .gitlab-ci.yml
        app.py                              <--- Точка входа, где только импорт и запуск
        congig.py                           <--- Конфигурация приложения
        CONTRIBUTING.md
        coverage.xml
        daily_git_commit.py                 <--- Функция автосохранения проекта
        docker-compose.yml
        Dockerfile
        LICENSE.txt
        Makefile
        README.md
        requiments.txt                      <--- Не все указанные используются
    /logs
        access.log                          <--- s ссылка на /var/log/nginx/access.log
        error.log                           <--- s ссылка на /var/log/nginx/error.log
        flask.log                           <--- s ссылка на /var/log/local.work/flask.log
        gunicorn.access.log                 <--- логи гуникорна
        gunicorn.error.log                  <--- логи гуникорна 
    /shared             <--- Общая директория между VM и хостом. Отключена
    /venv    
```

# 3: Создайте файл Flask-приложения (app.py)
Теперь создадим все файлы. 

# Код для `app.py`:

```python
from flask import Flask
from routes.main import main
from routes.api import api
from routes.auth_routes import auth
from routes.admin import admin
from threading import Thread

# Секретные секреты
app = Flask(__name__, static_folder='static', template_folder='/var/www/local.work/templates')
app.secret_key = 'fucking_incredibly_secret_key'
app.register_blueprint(main)
app.register_blueprint(api)
app.register_blueprint(auth)
app.register_blueprint(admin)

# Функция для запуска сервера на другом порту
def run_on_port(port):
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)

# Запуск приложения
if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    # Запускаем два экземпляра Flask на разных портах
    thread_1 = Thread(target=run_on_port, args=(5000,))
    thread_2 = Thread(target=run_on_port, args=(8000,))

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()
```
# Код для `fetch_data.py`:

```python
import requests
import json

def fetch_data():
    url = "http://10.121.1.40:8080/employee-changes?"
    
    # Отключаем прокси-серверы
    proxies = {
        "http": None,
        "https": None
    }
    
    try:
        # Выполняем запрос с отключением прокси
        response = requests.get(url, proxies=proxies)
        
        # Проверяем, успешно ли выполнен запрос
        if response.status_code == 200:
            # Парсим ответ JSON
            data = response.json()
            
            # # Выводим данные до изменения
            # print("Данные до изменений:")
            # for item in data:
            #     print(item)
            
            # Пробуем обработать данные без изменений
            for item in data:
                # Оставляем строки как есть, без изменений
                item['name'] = item['name']
                item['position'] = item['position']
                item['department'] = item['department']
                item['branch'] = item['branch']
            
            # # Выводим данные после изменения
            # print("Данные после изменений:")
            # for item in data:
            #     print(item)
            
            # Пишем результат в файл
            with open("/var/www/local.work/data/employee.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
            print("Данные успешно получены и записаны в файл.")
        else:
            print(f"Ошибка при запросе данных: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе данных: {e}")

# Запуск функции для получения данных
fetch_data()
```

# Код для `admin.py`:

```python
from flask import Blueprint, send_from_directory
import os, shutil, glob
from flask import jsonify

admin = Blueprint('admin', __name__)

TEMPLATE_PATTERN = '/var/www/shared/*.xlsb'
DEST_FILE = '/var/www/html/shared/Представительские.xlsb'

@admin.route('/admin/<path:filename>')
def admin_files(filename):
    return send_from_directory('/var/www/local.work/admin', filename)

@admin.route('/shared/<filename>')
def download_file(filename):
    return send_from_directory('/var/www/html/shared', filename)

@admin.route('/images/<filename>')
def send_image(filename):
    return send_from_directory('/var/www/local.work/images', filename)

@admin.route('/copy-file', methods=['POST'])
def copy_file():
    try:
        files = glob.glob(TEMPLATE_PATTERN)
        if not files:
            return jsonify({'message': 'Файл не найден', 'status': 'error'}), 404
        
        source_file = files[0]
        
        # Проверка, существует ли файл назначения, и его удаление для перезаписи
        if os.path.exists(DEST_FILE):
            os.remove(DEST_FILE)

        # Копирование файла с заменой
        shutil.copy(source_file, DEST_FILE)
        return jsonify({'message': 'Файл успешно скопирован и заменен!', 'status': 'success'}), 200
    except Exception as e:
        return jsonify({'message': f'Ошибка при копировании файла: {e}', 'status': 'error'}), 500
```

# Код для `api.py`:

```python
from flask import Blueprint, jsonify, request
from core.db import load_registry, save_registry, get_employee_info
import os

api = Blueprint('api', __name__)

# Удаление записи по индексу
@api.route('/api/registry/delete/<int:index>', methods=['POST'])
def delete_entry(index):
    records = load_registry()

    # Проверяем, что индекс существует
    if index < 0 or index >= len(records):
        return jsonify({'error': 'Запись не найдена'}), 404

    # Удаляем запись по индексу
    records.pop(index)
    save_registry(records)

    return jsonify({'message': 'Запись удалена успешно'}), 200

# Подтверждение затрат
@api.route('/api/registry/approve/<int:index>', methods=['POST'])
def approve_entry(index):
    try:
        print(f"Получен запрос на согласование записи с индексом {index}")  # Логируем начало работы
        data = load_registry()
        # print(f"Загружены данные реестра: {data}")  # Логируем загруженные данные
        
        if 0 <= index < len(data):
            payload = request.get_json()    # Обработка role через request.get_json()
            role = payload.get('role', '')
            print(f"Роль пользователя: {role}")  # Логируем роль, чтобы увидеть, что передается

            # Обновляем запись в зависимости от роли
            if data[index]:
                if role == 'neiger':
                    data[index]['approved'] = 'Согласовано Нейгером'
                else:
                    data[index]['approved'] = 'Согласовано'

                save_registry(data)  # сохраняю изменения
                return jsonify({'message': 'Запись успешно согласована'}), 200  # отправляю jsonify()
            else:
                print(f"Ошибка: запись с индексом {index} не найдена")
                return jsonify({'message': 'Запись не найдена'}), 404
        else:
            print(f"Ошибка: индекс {index} вне диапазона данных")
            return jsonify({'message': 'Неверный индекс'}), 404
    except Exception as e:
        print(f"Ошибка при обработке запроса: {e}")  # Логируем исключение
        return jsonify({'message': f'Ошибка: {e}'}), 500

# Отклонение затрат
@api.route('/api/registry/reject/<int:index>', methods=['POST'])
def reject_entry(index):
    try:
        records = load_registry()
        if 0 <= index < len(records):
            records[index]['approved'] = 'Не согласовано'
            save_registry(records)
            return '', 204
        else:
            return 'Индекс вне диапазона', 400
    except Exception as e:
        print(f"Ошибка при отклонении записи: {e}")
        return 'Ошибка сервера', 500

# Маршрут для обработки ввода ФИО сотрудника
@api.route('/check_employee', methods=['POST']) # Если клиент отправит POST-запрос по адресу /check_employee, вызови функцию check_employee()
def check_employee():
    print("✔ check_employee вызван")
    data = request.get_json()                   # данные принимаются из js
    print(f"Получено имя: {data}")
    employee_name = data.get('employeeName')    # возвращается введённое ФИО сотрудника

    result = get_employee_info(employee_name)   # Возвращает либо словарь с данными, либо None
    if result:
        return jsonify({"status": "found", "data": result}) # Это формирует ответ в формате JSON, который отправляется обратно в браузер (фронтенду).
    else:
        return jsonify({"status": "not_found", "message": "Указанный сотрудник не состоит в штате организации. Пожалуйста, введите корректное ФИО."}), 404

# Маршрут для актуализации данных по сотрудникам
@api.route('/update_employees', methods=['POST'])
def update_employees():
    try:
        # Здесь вызывается скрипт для актуализации данных сотрудников
        os.system('python /var/www/local.work/fetch_data.py')  # Запуск скрипта
        return jsonify({"status": "success", "message": "Список сотрудников успешно обновлён"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
```

# Код для `auth_routes.py`:

```python
from core.auth import users, user_display_names, admin_users, approvers, viewers, neiger
from flask import Blueprint, request, session, redirect, render_template, url_for

auth = Blueprint('auth', __name__)

# маршрут где данне из index.html направляются в login а дальше передаются в registry.html
@auth.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Проверка логина и пароля и раздача ролей
    if username in users and users[username] == password:
        session['username'] = username
        session['display_name'] = user_display_names.get(username, username)    # задаю имена для отображения

        # раздача ролей
        if username in admin_users:
            session['role'] = 'admin'
        elif username in approvers:
            session['role'] = 'approver'
        elif username in neiger:
            session['role'] = 'neiger'
        elif username in viewers:
            session['role'] = 'viewer'
        else:
            session['role'] = 'viewer'

        return redirect(url_for('main.registry_page'))  # После входа — на страницу реестра
    # Возврат на форму входа с сообщением об ошибке
    return render_template('index.html', error='Неверный логин или пароль')

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('main.index'))
```

# Код для `main.py`:

```python
from flask import Blueprint, render_template, session, redirect, url_for, request
from core.db import load_registry, save_registry
from datetime import datetime, timedelta
from num2words import num2words

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/input', methods=['GET', 'POST'])
def input_page():
    # Инициализация переменных по умолчанию
    memo_number = ""
    memo_date = ""
    act_date = ""
    formatted_expenses = ""
    employee_name = ""
    expenses_text = ""

    if request.method == 'POST':
        # Получение данных из формы
        employee_name = request.form.get('employeeName')
        position = request.form.get('position')
        branch = request.form.get('branch')
        department = request.form.get('department')
        meeting_purpose = request.form.get('meetingPurpose')
        organization_name = request.form.get('organizationName')
        organization_inn = request.form.get('organizationInn')
        negotiation_result = request.form.get('negotiationResult')
        expenses = request.form.get('expenses')
        event_date = request.form.get('eventDate')
        event_location = request.form.get('eventLocation')
        pm_representatives = request.form.getlist('pmRepresentatives[]')
        org_representatives = request.form.getlist('orgRepresentatives[]')
        infotex_representatives = request.form.getlist('infotexRepresentatives[]')

    # Преобразуем expenses в финансовый формат
        try:
            # Заменим запятую на точку для преобразования
            expenses_float = float(expenses.replace(',', '.'))
            # Форматируем с двумя знаками после запятой, пробелами между тысячами, запятой как разделителем
            formatted_expenses = '{:,.2f}'.format(expenses_float).replace(',', ' ').replace('.', ',')
            # Преобразуем число в текст
            expenses_text = num2words(int(expenses_float), lang='ru').lower().capitalize()
        except:
            formatted_expenses = expenses  # если ошибка — оставляем как есть
        
    # Вычисляем даты
        try:
            if not event_date:
                raise ValueError("Дата события не была передана или пустая строка.")
            date_obj = datetime.strptime(event_date, "%Y-%m-%d")
            memo_date = date_obj - timedelta(days=5)
            act_date = date_obj + timedelta(days=5)
            memo_number = f"{memo_date.strftime('%d%m%Y')}-1" 
            memo_date = memo_date.strftime('%d.%m.%Y')  # дата, которая попадает в служебную записку -5 дней от даты события
            act_date = act_date.strftime('%d.%m.%Y')    # дата, которая попадает в акт и отчёт +5 дней от даты события
            event_date = date_obj.strftime('%d.%m.%Y')  # дата события в русском формате
        except ValueError as ve: # Обработка ошибки, если дата не была передана или имеет неверный формат
            print(f"Ошибка при обработке даты: {ve}")  # Логирование ошибки
        except Exception as e:
            memo_number = "СЗ-???????"  # если что-то пошло не так
            print(f"Ошибка при обработке даты: {e}")  # Логирование ошибки
    # Форматируем ФИО: Фамилия, Имя, Отчество
        if employee_name:
            name_parts = employee_name.split()
            if len(name_parts) >= 1:
                surname = name_parts[0].capitalize()  # Фамилия с заглавной
            else:
                surname = ""
            if len(name_parts) >= 2:
                first_name = name_parts[1].capitalize()  # Имя с заглавной
            else:
                first_name = ""
            if len(name_parts) >= 3:
                patronymic = name_parts[2].capitalize()  # Отчество с заглавной
            else:
                patronymic = ""

            # Собираем назад в строку с точками после имени и отчества
            formatted_employee_name = f"{surname} {first_name[0]}. {patronymic[0]}." if first_name or patronymic else f"{surname}"
        else: formatted_employee_name = ""

            # Сохраняем всё в сессию
        session['form_data'] = {
            'employee_name': formatted_employee_name,
            'position': position,
            'branch': branch,
            'department': department,
            'meeting_purpose': meeting_purpose,
            'organization_name': organization_name,
            'organization_inn': organization_inn,
            'negotiation_result': negotiation_result,
            'expenses': formatted_expenses,
            'event_date': event_date,
            'event_location': event_location,
            'memo_date': memo_date,
            'act_date': act_date,
            'pm_representatives': pm_representatives,
            'org_representatives': org_representatives,
            'infotex_representatives': infotex_representatives,
            'memo_number': memo_number,
            'expenses_text': expenses_text,
            'approved': 'Не рассмотрено'
        }

        # ⬇️ Сохраняем в файл после того как словарь сохранён в сессию
        registry = load_registry()
        registry.append(session['form_data'])
        save_registry(registry)
        print("Данные формы получены, сохраняем в JSON")
        # send_new_entry_notification()
        # print("Информация о новой записи отправлена по электронной почте")        

    # После сохранения в сессию — перенаправляем пользователя на страницу с результатом
        return redirect(url_for('main.preview_all'))
        
    # Для GET-запроса возвращаем форму
    return render_template('input.html')

@main.route('/preview_all')
def preview_all():
    form_data = session.get('form_data')
    if not form_data:
        return "Нет данных для отображения", 400
    return render_template('preview_all.html', form_data=form_data)

@main.route('/print_form')
def print_form():
    if request.method == 'POST':
        print("Получен неожиданный POST на /print_form")
    data = session.get('form_data', {})
    return render_template('print_form.html', **data)

@main.route('/act')
def act():
    data = session.get('form_data', {})
    return render_template('act.html', **data)

@main.route('/report')
def report():
    data = session.get('form_data', {})
    return render_template('report.html', **data)

# registry получает данные из login
@main.route('/registry')
def registry_page():
    if 'username' not in session:
        return redirect(url_for('index'))   # Если пользователь не авторизован, перенаправляем на страницу входа

    username = session['username']
    display_name = session.get('display_name', username)  # здесь я передаю display_name из login в rigistry
    role = session.get('role', 'viewer')  # по умолчанию только просмотр

    try:
        all_records  = load_registry()   # Загружаем записи из файла
    except Exception as e:
        all_records  = []    # Если произошла ошибка — оставляем список пустым
        print(f"Ошибка при загрузке реестра: {e}")  # Логирование ошибки

    records = []
    for idx, record in enumerate(all_records):
        # Фильтрация по роли
        if role == 'neiger':
            dept = (record.get('department') or '').lower()
            if 'коммерческий департамент' in dept:
                record_with_index = record.copy()
                record_with_index['global_index'] = idx
                records.append(record_with_index)
        else:
            # Для остальных ролей показываем всё
            record_with_index = record.copy()
            record_with_index['global_index'] = idx
            records.append(record_with_index)

    return render_template('registry.html', records=records, username=username, role=role, display_name=display_name)
```

# Код для `auth.py`:

```python
from flask import Blueprint, request, session, redirect, render_template, url_for



# Пользователи
users = {
    "admin": "adminpft,fkb",
    "Irina.Dedeshko@infotecs.ru": "dedeshko123",
    "Irina.Zvontsova@infotecs.ru": "zvontsova456",
    "Roman.Kobtsev@amonitoring.ru": "kobtsev789",
    "Sergey.Neyger@amonitoring.ru": "S3rNey#Monitor25!"
}
user_display_names = {
    "Roman.Kobtsev@amonitoring.ru": "Кобцев Роман",
    "Irina.Dedeshko@infotecs.ru": "Дедешко Ирина",
    "Irina.Zvontsova@infotecs.ru": "Звонцова Ирина",
    "Sergey.Neyger@amonitoring.ru": "Нейгер Сергей",
    "admin": "Администратор"
}

# Разделение ролей
admin_users = ['admin']
approvers = ['Roman.Kobtsev@amonitoring.ru', 'admin']
viewers = ['Irina.Dedeshko@infotecs.ru', 'Irina.Zvontsova@infotecs.ru']
neiger = ['Sergey.Neyger@amonitoring.ru']
```

# Код для `db.py`:

```python
import json, os

REGISTRY_FILE = '/var/www/local.work/data/registry.json'
EMPLOYEE_FILE = '/var/www/local.work/data/employee.json'

# Загрузка реестра записей
def load_registry():
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# Сохранение реестра записей
def save_registry(registry):
    with open(REGISTRY_FILE, 'w', encoding='utf-8') as f:
        json.dump(registry, f, ensure_ascii=False, indent=4)

# Получение записей из БД MSSQL
def get_employee_info(employee_name):
    try:
        with open(EMPLOYEE_FILE, 'r', encoding='utf-8') as file:
            employees = json.load(file)

        # Ищем сотрудника по имени
        for employee in employees:
            if employee['name'] == employee_name:
                return {
                    'position': employee['position'],
                    'branch': employee['branch'],
                    'department': employee['department']
                }
        return None
    except (FileNotFoundError, json.JSONDecodeError):
        return None
```

### Шаг 4: Создадим HTML страницы

#### Код для `act.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Служебная записка</title>
    <!-- Указываем путь к фавикону -->
    <link rel="icon" href="{{ url_for('static', filename='ico.ico') }}" type="image/x-icon">
    <link rel="stylesheet" href="/static/css/act.css">
</head>
<body>
    <!-- Кнопка для печати -->
    <!-- <button class="print_button" onclick="window.print()">Просмотр и печать</button> -->

    <!-- Кнопка перехода на следующую страницу -->
    <!-- <button class="next_page_button" onclick="window.location.href='/report'">Следующая страница</button> -->
    <!-- Кнопка возврата на предыдущую страницу -->
    <!-- <button class="previos_page_button" onclick="window.location.href='/print_form'">Предыдущая страница</button> -->

    <!-- Основной контейнер -->
    <main class="container" role="document" aria-label="Акт">
            <!-- Верхний блок -->
            <table class="transparent-table">
                <tr>
                    <td style="font-weight: bold; padding-left: 80px; padding-top: 10px;">АО "ПМ"</td>
                    <td></td> <!-- Пустая ячейка для выравнивания с нижней строкой -->
                    <td style="text-align: right; padding-right: 80px; padding-top: 10px;">УТВЕРЖДАЮ</td>
                </tr>
                <tr>
                    <td td style="font-weight: bold; padding-left: 50px; font-size: 10px;">Наименование организации</td>
                    <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    <td style="text-align: right; padding-right: 20px;">Генеральный директор АО «ПМ»</td>
                </tr>
                <tr>
                    <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    <td style="text-align: right; padding-right: 20px;">Кобцев Р. Ю.</td>
                </tr>
                <tr>
                    <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    <td style="height: 10px; text-align: right; padding-right: 20px;">_____________________________</td>
                </tr>
                <tr>
                    <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    <td style="height: 10px; text-align: right; padding-right: 120px; font-size: 10px; color: #888;">(подпись)</td>
                </tr>
            </table>
            
        <section class="content">
            <!-- Шапка -->
            <table class="transparent-table">
                <tr>
                    <td style="text-align: center;">Акт</td>
                </tr>
                <tr>
                    <td style="text-align: center;">на списание представительских расходов</td>
                </tr>
                <tr>
                    <td style="text-align: center; font-weight: bold"> от {{ act_date }} </td>
                </tr>
                <tr>
                    <td style="text-align: center;">Комиссия, назначенная приказом № 2014/01/09-1 от 09.01.2014 г. составила настоящий Акт от</td>
                </tr>
                <tr>
                    <td style="text-align: center;">{{ act_date }} о списании представительских расходов в сумме </td>
                </tr>
                <tr>
                    <td style="font-weight: bold; text-align: center;">{{ expenses_text }} </td>
                </tr>
                <tr><td style="height: 10px; font-weight: bold"></td> <!-- Пустая ячейка с высотой --></tr>
            </table>

            <!-- Содержание записки -->
                <!-- Сведения -->
                <table class="table">
                    <tr>
                        <td colspan="2" style="font-weight: bold; border-top: 2px solid black; border-left: 2px solid black; border-right: 2px solid black;"> Дополнительные сведения:</td>
                    </tr>
                    <tr>
                        <td style="width: 60%;border-left: 2px solid black;"> Дата проведения приема: </td>
                        <td style="width: 40%;font-weight: bold; border-right: 2px solid black;"> {{ event_date }} </td>
                    </tr>
                    <tr>
                        <td style="width: 60%;border-left: 2px solid black;"> Место проведения приема: </td>
                        <td style="width: 40%;font-weight: bold; border-right: 2px solid black;"> {{ event_location }} </td>
                    </tr>
                    <tr>
                        <td style="width: 60%;border-left: 2px solid black; border-bottom: 2px solid black;"> Служебное задание: </td>
                        <td style="width: 40%;font-weight: bold; border-bottom: 2px solid black; border-right: 2px solid black;"> {{ memo_number }} </td>
                    </tr>
                </table>

                <!-- пустая строка -->
                <table class="transparent-table">
                    <tr>
                        <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    </tr>
                </table>

                <!-- Приглашённые лица ПМ -->
                <table class="transparent-table">
                    <tr>
                        <td style="font-weight: bold;">Приглашенные лица со стороны АО «ПМ»</td>
                    </tr>
                </table>
                <table class="table">
                    <tr>
                        <td style="width: 60%;font-weight: bold; border-top: 2px solid black; border-left: 2px solid black; border-bottom: 2px solid black; text-align: left; vertical-align: top;">
                            В составе:
                        </td>
                        <td style="width: 40%;font-weight: bold; border-top: 2px solid black; border-right: 2px solid black; border-bottom: 2px solid black;"> 
                            {% for rep in pm_representatives %}
                                {{ rep }}<br>
                            {% endfor %}
                        </td>
                    </tr>
                </table>

                <!-- пустая строка -->
                <table class="transparent-table">
                    <tr>
                        <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    </tr>
                </table>

                <!-- Приглашённые лица другой организации -->
                <table class="transparent-table">
                    <tr>
                        <td style="font-weight: bold;">Приглашенные лица со стороны {{  organization_name }}</td>
                    </tr>
                </table>
                <table class="table">
                    <tr>
                        <td style="width: 60%;font-weight: bold; border-top: 2px solid black; border-left: 2px solid black; border-bottom: 2px solid black; text-align: left; vertical-align: top;">
                            В составе:
                        </td>
                        <td style="width: 40%;font-weight: bold; border-top: 2px solid black; border-right: 2px solid black; border-bottom: 2px solid black;"> 
                            {% for rep in org_representatives %}
                                {{ rep }}<br>
                            {% endfor %}
                        </td>
                    </tr>
                </table>

                <!-- пустая строка -->
                <table class="transparent-table">
                    <tr>
                        <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    </tr>
                </table>

                <!-- Приглашённые лица Инфотекс -->
                <table class="transparent-table">
                    <tr>
                        <td style="font-weight: bold;">Приглашенные лица со стороны АО "ИнфоТеКС"</td>
                    </tr>
                </table>
                <table class="table">
                    <tr>
                        <td style="width: 60%;font-weight: bold; border-top: 2px solid black; border-left: 2px solid black; border-bottom: 2px solid black; text-align: left; vertical-align: top;">
                            В составе:
                        </td>
                        <td style="width: 40%;font-weight: bold; border-top: 2px solid black; border-right: 2px solid black; border-bottom: 2px solid black;"> 
                            {% for rep in infotex_representatives %}
                                {{ rep }}<br>
                            {% endfor %}
                        </td>
                    </tr>
                </table>

                <!-- пустая строка -->
                <table class="transparent-table">
                    <tr>
                        <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    </tr>
                </table>

                <!-- Итог -->
                <table class="table">
                    <tr>
                        <td style="width: 10%;font-weight: bold; border-top: 2px solid black; border-left: 2px solid black; font-size: 12px; text-align: center;">№ п/п</td>
                        <td style="width: 50%;font-weight: bold; border-top: 2px solid black; font-size: 12px; text-align: center;"> Вид представительских расходов</td>
                        <td style="width: 40%;font-weight: bold; border-top: 2px solid black; border-right: 2px solid black; font-size: 12px; text-align: center;"> Сумма (руб.)</td>
                    </tr>
                    <tr>
                        <td style="font-weight: bold; border-left: 2px solid black; text-align: center;">1</td>
                        <td style="font-weight: bold;">Буфетное обслуживание </td>
                        <td style="font-weight: bold;border-right: 2px solid black; text-align: center;">{{ expenses  }} рублей</td>
                    </tr>
                    <tr>
                        <td style="border-bottom: 2px solid black; border-left: 2px solid black;"></td>
                        <td style="font-weight: bold; border-bottom: 2px solid black;">Итого:</td>
                        <td style="font-weight: bold; border-bottom: 2px solid black; border-right: 2px solid black; text-align: center;">{{ expenses  }} рублей</td>
                    </tr>
                </table>

                <!-- пустая строка -->
                <table class="transparent-table">
                    <tr>
                        <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    </tr>
                </table>

                <!-- Низ -->
            <table class="transparent-table">
                <tr>
                    <td style="width: 10%;  text-align: left;">Всего:</td>
                    <td style="font-weight: bold; width: 90%; text-align: center;">{{ expenses_text  }}</td>
                </tr>
            </table>

            <!-- пустая строка -->
            <table class="transparent-table">
                <tr>
                    <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                </tr>
            </table>

            <table class="transparent-table">
                <tr>
                    <td style="text-align: left;">Первичные документы, подтверждающие расходы  находятся в авансовом отчете (расходном ордере):</td>
                </tr>
            </table>
            <!-- пустая строка -->
            <table class="transparent-table">
                <tr>
                    <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                </tr>
            </table>
            <table class="transparent-table">
                <tr>
                    <td style="height: 10px; border-bottom: 1px solid black;"></td>
                </tr>
            </table>
            <table class="transparent-table">
                <tr>
                    <td style="height: 10px; text-align: center; font-size: 14px; color: #888;">(заполняется сотрудником бухгалтерии)</td>
                </tr>
            </table>
            <!-- пустая строка -->
            <table class="transparent-table">
                <tr>
                    <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                </tr>
            </table>
            <table class="transparent-table">
                <tr>
                    <td style="width: 50%;  text-align: left; font-weight: bold;">Признать затраты в сумме :</td>
                    <td style="width: 50%; text-align: center; font-weight: bold;">{{ expenses  }} рублей</td>
                </tr>
                <tr>
                    <td colspan="2" style="text-align: left;">на представительское мероприятие c участниками деловых переговоров, </td>
                </tr>
                <tr>
                    <td colspan="2" style="text-align: left;">не превысившими установленную смету, согласно служебного задания.</td>
                </tr>
            </table>
            <!-- пустая строка -->
            <table class="transparent-table">
                <tr>
                    <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                </tr>
            </table>
            <table class="transparent-table">
                <tr>
                    <td colspan="3" style=" font-weight: bold;">Председатель комиссии:</td>                    
                </tr>
                <tr>
                    <td style="width: 33%; height: 10px; border-bottom: 1px solid black; text-align: center;">Генеральный директор</td>
                    <td style="width: 33%; font-weight: bold; border-bottom: 1px solid black;"></td>
                    <td style="width: 33%; font-weight: bold; border-bottom: 1px solid black; text-align: center;">Кобцев Р.Ю.</td>
                </tr>
                <tr>
                    <td style="width: 33%; height: 10px; text-align: center; font-size: 14px; color: #888;">(должность)</td>
                    <td style="width: 33%; height: 10px; text-align: center; font-size: 14px; color: #888;">(подпись)</td>
                    <td style="width: 33%; height: 10px; text-align: center; font-size: 14px; color: #888;">(ФИО)</td>
                </tr>
            </table>
             <!-- пустая строка -->
             <table class="transparent-table">
                <tr>
                    <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                </tr>
            </table>
            <table class="transparent-table">
                <tr>
                    <td colspan="3" style=" font-weight: bold;">Председатель комиссии:</td>                    
                </tr>
                <tr>
                    <td style="width: 33%; height: 10px; border-bottom: 1px solid black; text-align: center;">Главный бухгалтер</td>
                    <td style="width: 33%; font-weight: bold; border-bottom: 1px solid black;"></td>
                    <td style="width: 33%; font-weight: bold; border-bottom: 1px solid black; text-align: center;">Дедешко И.А.</td>
                </tr>
                <tr>
                    <td style="width: 33%; height: 10px; text-align: center; font-size: 14px; color: #888;">(должность)</td>
                    <td style="width: 33%; height: 10px; text-align: center; font-size: 14px; color: #888;">(подпись)</td>
                    <td style="width: 33%; height: 10px; text-align: center; font-size: 14px; color: #888;">(ФИО)</td>
                </tr>
            </table>
        </section>
    </main>
</body>                
```

#### Код для `index.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local Work</title>
    <!-- Указываем путь к фавикону -->
    <link rel="icon" href="{{ url_for('static', filename='ico.ico') }}" type="image/x-icon">
    <link rel="stylesheet" href="/static/css/start_page.css?v=2">
</head>
<body>
    <header>
        <h1>Добро пожаловать!</h1>
    </header>
    <main>
        <section>
            <!-- <h2>Здесь вы можете скачать актуальную версию файла для отчёта по представительским расходам АО "ПМ".</h2>
            <p>Нажмите на <a href="/shared/Представительские.xlsb">ссылку</a>, чтобы скачать excel файл.</p>
            <p>Обратите внимание на то, что браузер может задать вопрос о необходимости сохранения файла.</p>
            <p>В случае возникновения сообщения - необходимо подтвердить действие.</p>
            <p>В скаченном файле рекомендуется включить содержимое для корректной работы макросов добавления строк.</p>
            <p>Либо, имеется возможность интерактивно заполнить данные, перейдя по кнопке ниже.</p> -->
            <h2>Здесь вы можете заполнить отчёт по представительским расходам АО "ПМ".</h2>
        </section>
	<section>
        <!-- Кнопка для перехода на страницу заполнения данных -->
        <button class="form_button" onclick="location.href='/input'">Перейти к заполнению данных</button>
	    <button class="admin-button" onclick="location.href='/admin/login.html'">⚙️ Админ-панель</button>
	</section>
    <section class="login-container">
        <h2>Авторизация</h2>
        <form method="POST" action="/login">
            <label for="username">Логин:</label>
            <input type="text" id="username" name="username" required>
        
            <label for="password">Пароль:</label>
            <input type="password" id="password" name="password" required>
        
            <button type="submit">Войти</button>
        </form>
        {% if error %}
        <p style="color:red;">{{ error }}</p>
        {% endif %}
    </section>
    <script src="/static/js/index.js"></script>
    </main>
    <footer>
        <p>&copy; 2025 Wish you a successfull and productive trip</p>
    </footer>
</body>
</html>
```

#### Код для `input.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Форма ввода информации</title>
    <!-- Указываем путь к фавикону -->
    <link rel="icon" href="{{ url_for('static', filename='ico.ico') }}" type="image/x-icon">
    <link rel="stylesheet" href="/static/css/input.css">
</head>
<body>
    <!-- Кнопка возврата на предыдущую страницу -->
    <!-- <button class="previos_page_button" onclick="window.location.href='/'">Предыдущая страница</button> -->
    <div class="container">
        <h1>Форма ввода информации о встрече</h1>
        <form id="meetingForm" method="POST" action="{{ url_for('main.input_page') }}" target="_blank"> <!-- target="_blank" заставляет браузер открыть результат отправки формы в новой вкладке. -->
            <div class="form-group">
                <label for="employeeName">ФИО сотрудника:<span class="required">*</span></label>
                <input type="text" id="employeeName" name="employeeName" required>
                <!-- <input type="text" id="employeeName" name="employeeName" required oninput="checkEmployee()"> -->
            </div>
            
            <div class="form-group">
                <label for="position">Должность:</label>
                <input type="text" id="position" name="position" >
            </div>

            <div class="form-group">
                <label for="branch">Обособленное подразделение:</label>
                <input type="text" id="branch" name="branch" >
            </div>

            <div class="form-group">
                <label for="department">Отдел:</label>
                <input type="text" id="department" name="department" >
            </div>

            <div class="form-group">
                <label for="meetingPurpose">Цель встречи:<span class="required">*</span></label>
                <input type="text" id="meetingPurpose" name="meetingPurpose" required>
            </div>

            <div class="form-group">
                <label for="organizationName">Наименование организации с представителями которой проведена встреча:<span class="required">*</span></label>
                <input type="text" id="organizationName" name="organizationName" required>
            </div>

            <div class="form-group">
                <label for="organizationInn">ИНН организации:</label>
                <input type="text" id="organizationInn" name="organizationInn" >
            </div>

            <div class="form-group">
                <label for="orgRepresentatives">ФИО представителей организации:</label>
                <div id="orgRepresentatives">
                    <input type="text" name="orgRepresentatives[]">
                </div>
                <button type="button" id="addOrgRep">Добавить представителя организации</button>
            </div>

            <div class="form-group">
                <label for="infotexRepresentatives">ФИО представителей АО "ИнфоТеКС":</label>
                <div id="infotexRepresentatives">
                    <input type="text" name="infotexRepresentatives[]">
                </div>
                <button type="button" id="addInfotexRep">Добавить представителя АО "ИнфоТеКС"</button>
            </div>

            <div class="form-group">
                <label for="pmRepresentatives">ФИО представителей АО «ПМ»:</label>
                <div id="pmRepresentatives">
                    <input type="text" name="pmRepresentatives[]" value="">
                </div>
                <button type="button" id="addPmRep">Добавить представителя АО «ПМ»</button>
            </div>

            <div class="form-group">
                <label for="negotiationResult">Результат переговоров/встречи:<span class="required">*</span></label>
                <textarea id="negotiationResult" name="negotiationResult" required></textarea>
            </div>

            <div class="form-group">
                <label for="expenses">Сумма произведенных расходов:<span class="required">*</span></label>
                <input type="number" id="expenses" name="expenses" placeholder="Введите сумму" step="0.01" required>
            </div>

            <div class="form-group">
                <label for="eventDate">Дата мероприятия:<span class="required">*</span></label>
                <input type="date" id="eventDate" name="eventDate" required>
            </div>

            <div class="form-group">
                <label for="eventLocation">Место проведения:<span class="required">*</span></label>
                <input type="text" id="eventLocation" name="eventLocation" required>
            </div>

            <button type="submit" class="styled-button">Отправить</button>
            <!-- <button type="button" class="styled-button" onclick="submitForm()">Отправить</button> -->
        </form>
    </div>
    <script src="/static/js/input.js"></script>
</body>
</html>
```

#### Код для `preview_all.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>        
    <meta charset="UTF-8">
    <title>Предпросмотр всех документов</title>
    <!-- Указываем путь к фавикону -->
    <link rel="icon" href="{{ url_for('static', filename='ico.ico') }}" type="image/x-icon">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/preview_all.css') }}">
</head>
<body>
    <!-- <h1>Предпросмотр документов</h1> -->
    <button class="print_button" onclick="window.print()">Просмотр и печать</button>

    <!-- Подключаем страницы -->
    <iframe src="{{ url_for('main.print_form') }}"></iframe>
    <iframe src="{{ url_for('main.act') }}"></iframe>
    <iframe src="{{ url_for('main.report') }}"></iframe>

</body>
</html>
```

#### Код для `print_form.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Служебная записка</title>
    <!-- Указываем путь к фавикону -->
    <link rel="icon" href="{{ url_for('static', filename='ico.ico') }}" type="image/x-icon">
    <link rel="stylesheet" href="/static/css/print_form.css">
</head>
<body>
    <!-- Кнопка для печати -->
    <!-- <button class="print_button" onclick="window.print()">Просмотр и печать</button> -->

    <!-- Кнопка перехода на следующую страницу -->
    <!-- <button class="next_page_button" onclick="window.location.href='/act'">Следующая страница</button> -->
    <!-- Кнопка возврата на предыдущую страницу -->
    <!-- <button class="previos_page_button" onclick="window.location.href='/input'">Предыдущая страница</button> -->

    <!-- Основной контейнер -->
    <main class="container" role="document" aria-label="Служебная записка">
            <!-- Верхний блок -->
            <header class="header">
                <div class="top">
                    УТВЕРЖДАЮ
                </div>
                Генеральный директор АО «ПМ»<br>
                Кобцев Р. Ю.<br>                
                _____________________________<br>
                <div class="inscriptions low">
                    (подпись)
                </div>
            </header>

            <!-- Содержание записки -->
            <section class="content">
                <!-- Номер и дата -->
                <table class="transparent-table">
                    <tr>
                        <td>
                            Служебная записка <!-- № -->
                            <!-- <span class="bold">
                                {{ memo_number }}
                            </span>  -->
                                от 
                            <span class="bold">
                                {{ memo_date }}
                            </span>
                        </td>
                    </tr>
                </table>
                <!-- пустая строка -->
                <table class="transparent-table">
                    <tr>
                        <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    </tr>
                </table>                
                <!-- Исполнитель -->
                <table class="transparent-table">
                    <tr>
                        <td>
                            Кому: 
                            <span class="bold">
                                {{ employee_name }}
                            </span>
                        </td>
                    </tr>
                </table>
                <!-- пустая строка -->
                <table class="transparent-table">
                    <tr>
                        <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    </tr>
                </table> 
                <!-- Организация -->
                <table class="table">
                    <tr>
                        <td class="left-column">
                            Провести переговоры с представителями организации
                        </td>
                        <td class="right-column center">
                            <span class="bold">
                                {{ organization_name }}
                            </span>
                        </td>
                    </tr>
                </table>
                <!-- пустая строка -->
                <table class="transparent-table">
                    <tr>
                        <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    </tr>
                </table>
                <!-- Задача -->
                <table class="table">
                    <tr>
                        <td class="left-column">
                            Цель встречи:
                        </td>
                    </tr>
                    <tr>
                        <td class="left-column bold">
                            {{ meeting_purpose }}
                        </td>
                    </tr>
                </table>
                <!-- пустая строка -->
                <table class="transparent-table">
                    <tr>
                        <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    </tr>
                </table>
                <!-- Нотификация -->
                <table class="table">
                    <tr>
                        <td class="single-cell">
                            По результатам встречи представить отчёт в письменном виде, где отразить результаты переговоров и план дальнейшего взаимодействия с данным потенциальным клиентом.
                        </td>
                    </tr>
                </table>
                <!-- пустая строка -->
                <table class="transparent-table">
                    <tr>
                        <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    </tr>
                </table>
                <!-- Ещё нотификация -->
                <table class="table">
                    <tr>
                        <td class="single-cell">
                            <div>
                                Место проведения встречи предлагаю выбрать самостоятельно.
                            </div>
                        </td>
                    </tr>
                </table>
                <!-- пустая строка -->
                <table class="transparent-table">
                    <tr>
                        <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    </tr>
                </table>
                <!-- Предел суммы -->
                <table class="table">
                    <tr>
                        <td class="single-cell">
                            В случае возникновения представительских расходов установить предел расходов на одного человека не более
                        </td>
                    </tr>
                    <tr>
                        <td class="single-cell bold">
                            5 000,00 рублей <!-- {{ expenses }} рублей -->
                        </td>
                    </tr>
                </table>
                <!-- пустая строка -->
                <table class="transparent-table">
                    <tr>
                        <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    </tr>
                </table>                
                <!-- Последняя нотификация -->
                <table class="transparent-table">
                    <tr>
                        <td style="text-align: justify;">   <!-- Выраванивание по ширине -->
                            Компенсация расходов будет произведена при условии предоставления первичных отчётных документов, оформленных в соответствии с законодательством РФ.
                        </td>
                    </tr>
                </table>
                <!-- пустая строка -->
                <table class="transparent-table">
                    <tr>
                        <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    </tr>
                </table> 
                <!-- Подпись Генерального директора -->
                <table class="transparent-table">
                    <tr>
                        <td style="width: 33%; height: 10px; border-bottom: 1px solid black; text-align: center;">Генеральный директор</td>
                        <td style="width: 33%; font-weight: bold; border-bottom: 1px solid black;"></td>
                        <td style="width: 33%; font-weight: bold; border-bottom: 1px solid black; text-align: center;">Кобцев Р.Ю.</td>
                    </tr>
                    <tr>
                        <td style="width: 33%; height: 10px; text-align: center; font-size: 14px; color: #888;">(должность)</td>
                        <td style="width: 33%; height: 10px; text-align: center; font-size: 14px; color: #888;">(подпись)</td>
                        <td style="width: 33%; height: 10px; text-align: center; font-size: 14px; color: #888;">(ФИО)</td>
                    </tr>
                </table>
            </section>
    </main>
    <script src="/static/js/print_form.js"></script>
</body>
</html>
```

#### Код для `registry.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Реестр представительских расходов</title>
    <link rel="icon" href="{{ url_for('static', filename='ico.ico') }}" type="image/x-icon">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/registry.css') }}">
</head>
<body>
    <div class="container">
        <h1>Реестр записей</h1>
        <!-- Блок с информацией о пользователе и кнопкой выхода -->
        <p>Вы вошли как: <strong>{{ display_name }}</strong></p>
        <button class="logout-button" onclick="logout()">Выйти</button>

        {% if records %}
            <script>
                const userRole = "{{ role }}";
            </script>
            <table>
                <thead>
                    <tr>
                        <th style="text-align: center;">Имя сотрудника</th>
                        <th style="text-align: center;">Наименование организации с представителями которой проведена встреча</th>
                        <th style="text-align: center;">Цель встречи</th>
                        <th style="text-align: center;">Результат встречи</th>
                        <th style="text-align: center;">Сумма (₽)</th>
                        <th style="text-align: center;">Дата события</th>
                        <th style="text-align: center;">Согласовано</th>
                        {% if role in ['admin', 'approver', 'neiger'] %}
                            <th>Согласовать</th>
                        {% endif %}
                        {% if role == 'admin' %}
                            <th style="text-align: center;">Удалить</th>
                        {% endif %}
                    </tr>
                </thead>
                <tbody>
                    {% for record in records %}
                        <tr>
                            <td style="white-space: nowrap;">{{ record.get('employee_name', '') }}</td>
                            <td style="white-space: nowrap;">{{ record.get('organization_name', '') }}</td>
                            <td>{{ record.get('meeting_purpose', '') }}</td>
                            <td>{{ record.get('negotiation_result', '') }}</td>
                            <td style="white-space: nowrap; text-align: right; min-width: 100px;">
                                {{ record.get('expenses', '') }}
                            </td>
                            <td>{{ record.get('event_date', '') }}</td>
                            <td id="approved-cell-{{ record.global_index }}" style="text-align: center;">
                                {{ record.get('approved', '') }}
                            </td>
                                {% if role in ['admin', 'approver', 'neiger'] %}
                            <td>
                                <button class="approve" onclick="approveEntry({{ record.global_index }})">Согласовать</button>
                                <button class="reject" onclick="rejectEntry({{ record.global_index }})">Отклонить</button>
                            </td>
                            {% endif %}
                            {% if role == 'admin' %}
                                <td><button class="approve" onclick="deleteEntry({{ loop.index0 }})">Удалить</button></td>
                            {% endif %}
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% else %}
            <p>Нет доступных записей.</p>
        {% endif %}
    </div>
    <script src="{{ url_for('static', filename='js/registry.js') }}"></script>
</body>
</html>
```

#### Код для `report.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Служебная записка</title>
    <!-- Указываем путь к фавикону -->
    <link rel="icon" href="{{ url_for('static', filename='ico.ico') }}" type="image/x-icon">
    <link rel="stylesheet" href="/static/css/report.css">
</head>
<body>
    <!-- Кнопка для печати -->
    <!-- <button class="print_button" onclick="window.print()">Просмотр и печать</button> -->
    <!-- Кнопка возврата на предыдущую страницу -->
    <!-- <button class="previos_page_button" onclick="window.location.href='/act'">Предыдущая страница</button> -->

    <!-- Основной контейнер -->
    <main class="container" role="document" aria-label="Акт">
            <!-- Верхний блок -->
            <table class="transparent-table">
                <tr>
                    <td style="font-weight: bold; padding-left: 80px; "></td>
                    <td></td> <!-- Пустая ячейка для выравнивания с нижней строкой -->
                    <td style="text-align: right; padding-right: 80px; padding-top: 10px;">УТВЕРЖДАЮ</td>
                </tr>
                <tr>
                    <td td style="font-weight: bold; padding-left: 50px; font-size: 10px;"></td>
                    <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    <td style="text-align: right; padding-right: 20px;">Генеральный директор АО «ПМ»</td>
                </tr>
                <tr>
                    <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    <td style="text-align: right; padding-right: 20px;">Кобцев Р. Ю.</td>
                </tr>
                <tr>
                    <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    <td style="height: 10px; text-align: right; padding-right: 20px;">_____________________________</td>
                </tr>
                <tr>
                    <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    <td style="height: 10px; text-align: right; padding-right: 120px; font-size: 10px; color: #888;">(подпись)</td>
                </tr>
            </table>
            
        <section class="content">
            <!-- Шапка -->
            <table class="transparent-table">
                <tr>
                    <td style="text-align: center; font-weight: bold;">ОТЧЕТ от {{ act_date }}</td>
                </tr>
                <tr>
                    <td style="text-align: center; font-weight: bold;">о проведенных переговорах</td>
                </tr>
            </table>
            <br>

            <!-- Содержание записки -->
                <!-- Сведения -->
                <table class="table">
                    <tr>
                        <td style="width: 60%; font-weight: bold; border-top: 2px solid black; border-left: 2px solid black;"> Цель проведения переговоров с представителями</td>
                        <td style="width: 40%; text-align: center; font-weight: bold; border-top: 2px solid black; border-right: 2px solid black;">
                            {{ organization_name }}
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2" style="font-weight: bold; border-bottom: 2px solid black; border-right: 2px solid black; border-left: 2px solid black;"> {{ meeting_purpose }} </td>
                    </tr>
                </table>

                <!-- пустая строка -->
                <table class="transparent-table">
                    <tr>
                        <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    </tr>
                </table>

                <!-- Приглашённые лица другой организации -->
                <table class="table">
                    <tr>
                        <td style="width: 30%; border-top: 2px solid black; border-left: 2px solid black;"> В составе представителей от</td>
                        <td style="width: 70%; text-align: center; font-weight: bold; border-right: 2px solid black; border-top: 2px solid black;">
                            {{ organization_name }}
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2" style="font-weight: bold; border-right: 2px solid black; border-bottom: 2px solid black; border-left: 2px solid black;">
                            {% for rep in org_representatives %}
                                <div class="{% if not loop.last %}with-border{% endif %}">{{ rep }}</div>
                            {% endfor %}
                        </td>
                    </tr>
                </table>

                <!-- пустая строка -->
                <table class="transparent-table">
                    <tr>
                        <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    </tr>
                </table>

                <!-- Приглашённые лица ПМ -->
                <table class="table">
                    <tr>
                        <td style="border-top: 2px solid black; border-left: 2px solid black; border-right: 2px solid black;"> 
                            Со стороны АО «ПМ» присутствовало официальных представителей в составе:
                        </td>
                    </tr>
                    <tr>
                        <td style="font-weight: bold; border-right: 2px solid black; border-bottom: 2px solid black; border-left: 2px solid black;"> 
                            {% for rep in pm_representatives %}
                                <div class="{% if not loop.last %}with-border{% endif %}">{{ rep }}</div>
                            {% endfor %}
                        </td>
                    </tr>
                </table>

                <!-- пустая строка -->
                <table class="transparent-table">
                    <tr>
                        <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    </tr>
                </table>

                <!-- Приглашённые лица Инфотекс -->
                <table class="table">
                    <tr>
                        <td style="border-top: 2px solid black; border-left: 2px solid black; border-right: 2px solid black;"> 
                            Со стороны АО «ИнфоТеКС» присутствовало официальных представителей в составе:
                        </td>
                    </tr>
                    <tr>
                        <td style="font-weight: bold; border-right: 2px solid black; border-bottom: 2px solid black; border-left: 2px solid black;">
                            {% for rep in infotex_representatives %}
                                <div class="{% if not loop.last %}with-border{% endif %}">{{ rep }}</div>
                            {% endfor %}
                        </td>
                    </tr>
                </table>

                <!-- пустая строка -->
                <table class="transparent-table">
                    <tr>
                        <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    </tr>
                </table>

                <!-- Место -->
                <table class="table">
                    <tr>
                        <td style="width: 50%; font-weight: bold; border-top: 2px solid black; border-left: 2px solid black; text-align: left; border-bottom: 2px solid black; border-right: none;">
                            Местом проведения переговоров явилось
                        </td>
                        <td style="width: 50%; font-weight: bold; border-top: 2px solid black; border-right: 2px solid black; text-align: center; border-bottom: 2px solid black; border-left: none;">
                            {{ event_location }}
                        </td>
                    </tr>
                </table>

                <!-- пустая строка -->
                <table class="transparent-table">
                    <tr>
                        <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                    </tr>
                </table>

                <!-- Результат -->
            <table class="transparent-table">
                <tr>
                    <td style="width: 10%;  text-align: left;">В результате переговоров </td>
                </tr>
            </table>
            <table class="table">
                <tr>
                    <td style="font-weight: bold; border-top: 2px solid black; border-left: 2px solid black; font-size: 12px; border-bottom: 2px solid black; text-align: justify;">
                        {{ negotiation_result }}
                    </td>
                </tr>
            </table>

            <!-- пустая строка -->
            <table class="transparent-table">
                <tr>
                    <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                </tr>
            </table>

            <!-- Расходы -->
            <table class="transparent-table">
                <tr>
                    <td style="text-align: left;">В ходе переговоров были  произведены расходы в размере</td>
                    <td style="text-align: left; font-weight: bold;">{{ expenses }} рублей</td>
                </tr>
                <tr>
                    <td style="text-align: left;">Расходы документально подтверждены.</td>
                </tr>
            </table>
            
            <!-- пустая строка -->
            <table class="transparent-table">
                <tr>
                    <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                </tr>
            </table>
            <table class="transparent-table">
                <tr>
                    <td colspan="3" style=" font-weight: bold;">Подпись подотчётного лица </td>                    
                </tr>
                <tr>
                    <td style="width: 33%; height: 10px; border-bottom: 1px solid black; text-align: center;">{{ position }}</td>
                    <td style="width: 33%; font-weight: bold; border-bottom: 1px solid black;"></td>
                    <td style="width: 33%; font-weight: bold; border-bottom: 1px solid black; text-align: center;">{{ employee_name }}</td>
                </tr>
                <tr>
                    <td style="width: 33%; height: 10px; text-align: center; font-size: 14px; color: #888;">(должность)</td>
                    <td style="width: 33%; height: 10px; text-align: center; font-size: 14px; color: #888;">(подпись)</td>
                    <td style="width: 33%; height: 10px; text-align: center; font-size: 14px; color: #888;">(ФИО)</td>
                </tr>
            </table>
             <!-- пустая строка -->
             <table class="transparent-table">
                <tr>
                    <td style="height: 10px;"></td> <!-- Пустая ячейка с высотой -->
                </tr>
            </table>
            <table class="transparent-table">
                <tr>
                    <td colspan="3" style=" font-weight: bold;">Согласовано</td>                    
                </tr>
                <tr>
                    <td style="width: 33%; height: 10px; border-bottom: 1px solid black; text-align: center;">Генеральный директор</td>
                    <td style="width: 33%; font-weight: bold; border-bottom: 1px solid black;"></td>
                    <td style="width: 33%; font-weight: bold; border-bottom: 1px solid black; text-align: center;">Кобцев Р.Ю.</td>
                </tr>
                <tr>
                    <td style="width: 33%; height: 10px; text-align: center; font-size: 14px; color: #888;">(должность)</td>
                    <td style="width: 33%; height: 10px; text-align: center; font-size: 14px; color: #888;">(подпись)</td>
                    <td style="width: 33%; height: 10px; text-align: center; font-size: 14px; color: #888;">(ФИО)</td>
                </tr>
            </table>
        </section>
    </main>
</body>                
```

#### Код для `dashboard.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Управление файлами</title>
    <!-- Указываем путь к фавикону -->
    <link rel="icon" href="/static/ico/ico.ico" type="image/x-icon">
    <link rel="stylesheet" href="/static/css/dashboard.css"> 
</head>
<body>
    <!-- Контейнер для центрирования -->
    <div class="center-container">
        <!-- Кнопка для копирования файла -->
        <button id="copyFileBtn">Копировать файл</button>
        <!-- Кнопка для перехода на страницу заполнения данных -->
        <button id="goToInputPage" class="btn">Перейти к заполнению данных</button>
        <!-- Кнопка получения актуальных данных по сотрудникам -->
        <button id="refreshEmployeeData" class="btn">Актуализировать список сотрудников</button>
    </div>

    <!-- <script src="upload.js"></script> -->
    <script src="/static/js/dashboard.js"></script>
</body>
</html>
```

#### Код для `login.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Авторизация</title>
    <link rel="stylesheet" href="/static/css/auth.css">
</head>
<body>
    <div class="login-container">
        <h2>Вход администратора</h2>
        <form onsubmit="return login(event)">
            <label for="username">Логин:</label>
            <input type="text" id="username" required>
            
            <label for="password">Пароль:</label>
            <input type="password" id="password" required>
            
            <button type="submit">Войти</button>
        </form>
    </div>
    <script src="/static/js/auth.js"></script>
</body>
</html>
```

### Шаг 5: Создайте файл стилей (style.css)

#### Код для `act.css`:

```css
/* Стиль для печати и форматирование страницы A4 */
@page {
    size: A4 portrait;  /* или landscape при необходимости */
    margin: 2cm; /* Отступы по периметру страницы */
}

@media print {
    body {
        background: none !important;
        margin: 0;
        padding: 0;
    }

    * {
        box-shadow: none !important;
        background: none !important;
        color: black !important;
    }

    .container {
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        box-shadow: none !important;
        overflow: hidden;
        transform-origin: top left;
    }

    /* Скрыть всё вне .container */
    /* body > *:not(.container) {
        display: none !important;
    } */
}

/* Общие стили для содержимого страницы */
body {
    font-family: Times New Roman, Georgia, serif;
    background-color: rgb(248, 200, 124);
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
}
.container {    
    width: 50%;                                         /* Устанавливаем ширину контейнера на 50% от ширины родительского элемента */
    margin: 50px auto;                                  /* Автоматические отступы по бокам и 50px сверху и снизу, чтобы центрировать контейнер */    
    background-color: white;                          /* Устанавливаем белый фон для контейнера */    
    padding: 20px;                                       /* Внутренние отступы, чтобы текст не прилегал к краям контейнера */    
    border-radius: 8px;                                 /* Скругляем углы контейнера радиусом 8px */    
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);         /* Добавляем тень для контейнера, чтобы создать эффект "выпуклости" */
}
.low {
    font-size: 0.8em;      /* Уменьшаем размер шрифта */
    color: #888;           /* Меняем цвет текста на светло-серый */
    font-style: italic;    /* Делаем текст курсивом */
}

/* Содержание записки */
.content {
    margin-top: 40px;
    margin-bottom: 40px;
    font-size: 16px;
    line-height: 1.5;
    width: 100%; /* Убедимся, что контейнер растягивается на 100% ширины */
    box-sizing: border-box; /* Чтобы padding не выходил за пределы контейнера */
}

/* Стили для таблицы */
.table {
    position: relative;
    width: 100%;    /* Таблица будет занимать всю ширину контейнера */
    border-collapse: collapse;  /* Убираем двойные границы */
    line-height: 1;
}
.table td {
    border: 1px solid black; /* Жирные границы таблицы */
}

/* Стили для прозрачной таблицы */
.transparent-table {
    position: relative;
    width: 100%;
    border-collapse: collapse;
    line-height: 1;
}
.transparent-table td, 
.transparent-table th {
    border: none;
}




/* Стили для кнопки "Просмотр и печать" */
.print_button {
    position: absolute;
    top: 20px;
    left: 20px;
    background-color: white;
    color: #333;
    border: 2px solid #333;
    padding: 16px 32px;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    z-index: 1000;
}
.print_button:hover {
    background-color: #f0f0f0;
    transform: scale(1.05);
}
.print_button:active {
    transform: scale(1);
}

/* Стили для кнопки "Следующая страница" */
.next_page_button {
    position: absolute;
    top: 20px;
    right: 20px;
    background-color: white;
    color: #333;
    border: 2px solid #333;
    padding: 16px 32px;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    z-index: 1000;
}
.next_page_button:hover {
    background-color: #f0f0f0;
    transform: scale(1.05);
}
.next_page_button:active {
    transform: scale(1);
}

/* Стили для кнопки "Предыдущая страница" */
.previos_page_button {
    position: absolute;
    top: 100px;
    right: 20px;
    background-color: white;
    color: #333;
    border: 2px solid #333;
    padding: 16px 32px;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    z-index: 1000;
}
.previos_page_button:hover {
    background-color: #f0f0f0;
    transform: scale(1.05);
}
.previos_page_button:active {
    transform: scale(1);
}
```

#### Код для `auth.css`:

```css
/* Устанавливаем фон и выравнивание страницы */
body {
    margin: 0; /* Убираем внешние отступы у body */
    padding: 0; /* Убираем внутренние отступы у body */
    
    /* Фон. Можно использовать градиент (закомментировано ниже), 
       либо изображение фоном, как сейчас: */
    /* background: linear-gradient(to right, #667eea, #764ba2); /* красивый градиент */
    
    background: url("/images/Background2.png") no-repeat center center fixed; 
    /* Используем фоновое изображение, не повторяется, центрируется и фиксируется при прокрутке */
    
    background-size: cover; /* Растягивает изображение, чтобы покрывало весь экран */
    
    font-family: Arial, sans-serif; /* Устанавливаем шрифт */
    
    display: flex; /* Используем flexbox для центрирования */
    justify-content: center; /* Горизонтальное центрирование */
    align-items: center; /* Вертикальное центрирование */
    height: 100vh; /* Высота страницы — 100% от высоты экрана */
}

/* Стили для контейнера формы авторизации */
.login-container {
    background-color: white; /* Убираем прозрачность — делаем полностью белым */
    padding: 40px; /* Внутренний отступ */
    border-radius: 12px; /* Скругление углов */
    box-shadow: 0 8px 16px rgba(0,0,0,0.3); /* Тень для объёма */
    width: 350px; /* Ширина формы */
    text-align: center; /* Центрируем текст внутри */
}

/* Заголовок формы */
h2 {
    margin-bottom: 20px; /* Отступ снизу */
    color: #333; /* Тёмно-серый цвет текста */
}

/* Настройка формы и её элементов */
form {
    display: flex; /* Flexbox для вертикального выравнивания */
    flex-direction: column; /* Располагаем элементы столбцом */
}

/* Метки (текст "Логин", "Пароль") */
label {
    text-align: left; /* Выравнивание текста по левому краю */
    margin-bottom: 5px; /* Небольшой отступ снизу */
    font-weight: bold; /* Жирный текст */
    color: #444; /* Цвет текста */
}

/* Поля ввода */
input {
    padding: 10px; /* Внутренний отступ */
    margin-bottom: 15px; /* Отступ между полями */
    border: 1px solid #aaa; /* Серенькая рамка */
    border-radius: 6px; /* Скругление углов */
    font-size: 14px; /* Размер текста */
}

/* Кнопка входа */
button {
    background-color: #667eea; /* Синий фон */
    color: white; /* Белый текст */
    padding: 10px; /* Внутренний отступ */
    border: none; /* Без рамки */
    border-radius: 6px; /* Скругление углов */
    font-size: 16px; /* Размер текста */
    cursor: pointer; /* Курсор в виде руки при наведении */
    transition: background-color 0.3s; /* Плавный переход цвета при наведении */
}

/* Эффект при наведении на кнопку */
button:hover {
    background-color: #5a67d8; /* Немного темнее при наведении */
}
```

#### Код для `dashboard.css`:

```css
/* Стили для кнопки */
button {
    background-color: #4CAF50; /* Зеленый цвет фона */
    color: white; /* Белый цвет текста */
    font-size: 20px; /* Размер шрифта */
    padding: 20px 40px; /* Увеличенные отступы */
    border: none; /* Без рамки */
    border-radius: 10px; /* Скругленные углы */
    cursor: pointer; /* Указатель при наведении */
    box-shadow: 0 8px 16px rgba(0, 128, 0, 0.5); /* Тень для объема */
    transition: transform 0.3s, background-color 0.3s; /* Плавные изменения */
}

/* Эффект при наведении */
button:hover {
    background-color: #45a049; /* Темнее при наведении */
    /*transform: scale(1.1); /* Увеличиваем кнопку при наведении */
}

/* Эффект на активное состояние (при нажатии) */
button:active {
    transform: scale(1); /* Сбрасываем увеличение */
    box-shadow: 0 4px 8px rgba(0, 128, 0, 0.5); /* Уменьшаем тень */
}

/* Контейнер для центрирования */
.center-container {
    display: flex; /* Используем flexbox */
    justify-content: center; /* Центрируем по горизонтали */
    align-items: center; /* Центрируем по вертикали */
    width: 100%; /* Ширина 100% */
    height: 100%; /* Высота 100% */
}

/* Фон для этой страницы */
body {
    background-image: url("/images/background.png"); /* Путь к вашему изображению */
    background-size: cover;         /* Растягиваем изображение на всю доступную площадь */
    background-position: center center;  /* Центрируем изображение */
    background-repeat: no-repeat;    /* Запрещаем повторение изображения */
    height: 100vh;                  /* Устанавливаем высоту body на 100% высоты экрана */
    margin: 0;                      /* Убираем отступы */
    padding: 0;                     /* Убираем отступы */
}
```

#### Код для `input.css`:

```css
/* Общие стили для страницы */
body {
    font-family: 'Times New Roman', sans-serif;
    background-color: #f4f4f4;
    margin: 0;
    padding: 0;
}

.container {    
    width: 50%;                                         /* Устанавливаем ширину контейнера на 50% от ширины родительского элемента */
    margin: 50px auto;                                  /* Автоматические отступы по бокам и 50px сверху и снизу, чтобы центрировать контейнер */    
    background-color: white;                          /* Устанавливаем белый фон для контейнера */    
    padding: 20px;                                      /* Внутренние отступы, чтобы текст не прилегал к краям контейнера */    
    border-radius: 8px;                                 /* Скругляем углы контейнера радиусом 8px */    
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);         /* Добавляем тень для контейнера, чтобы создать эффект "выпуклости" */
}

/* Стили для обязательных полей */
/* <span class="required">*</span> */
.required {
    color: red; /* Красный цвет для звездочки */
    font-weight: bold; /* Жирный шрифт для звездочки */
    margin-left: 5px; /* Немного отступа между текстом и звездочкой */
}
input:required + .required,
textarea:required + .required {
    display: inline; /* Показываем звездочку только для обязательных полей */
}

h1 {
    text-align: center;
    margin-bottom: 20px;
}

form {
    display: flex;
    flex-direction: column;
}

.form-group {
    margin-bottom: 20px;
}

label {
    font-weight: bold;
    margin-bottom: 5px;
}

input, textarea {
    width: 100%;    /* Ширина поля ввода на 100% ширины контейнера */
    padding: 5px;  /* Уменьшаем правый отступ, оставляем остальное без изменений */
    font-size: 22px; /* Увеличиваем размер шрифта */
    margin-bottom: 15px;    /* Отступ снизу между полями ввода */
    border: 2px solid #ccc; /* Устанавливаем границу и цвет для поля ввода */
    border-radius: 5px; /* Скругляем углы поля ввода */
    background-color: #f0f0f0; /* Здесь задается цвет фона поля */
    font-family: 'Times New Roman', serif; /* Используем шрифт Times New Roman */
}

textarea {
    resize: vertical;
    min-height: 100px;
}

button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
    margin-top: 20px;
}

button:hover {
    background-color: #45a049;
}

button[type="button"] {
    background-color: #007BFF;
}

button[type="button"]:hover {
    background-color: #0056b3;
}

/* Стили для добавления дополнительных полей */
#orgRepresentatives, #infotexRepresentatives, #pmRepresentatives {
    margin-bottom: 10px;
}

#orgRepresentatives input, #infotexRepresentatives input, #pmRepresentatives input {
    margin-bottom: 10px;
}

/* Стиль для красивой кнопки */
.styled-button {
    background-color: #4CAF50; /* Зеленый цвет фона */
    color: white; /* Белый цвет текста */
    font-size: 18px; /* Размер шрифта */
    padding: 15px 30px; /* Отступы */
    border: none; /* Без рамки */
    border-radius: 25px; /* Скругленные углы */
    cursor: pointer; /* Указатель при наведении */
    box-shadow: 0 8px 16px rgba(0, 128, 0, 0.5); /* Тень для объема */
    transition: transform 0.3s, background-color 0.3s, box-shadow 0.3s; /* Плавные изменения */
    font-weight: bold; /* Сделаем шрифт жирным */
}

/* Эффект при наведении */
.styled-button:hover {
    background-color: #45a049; /* Темнее при наведении */
    transform: scale(1.05); /* Увеличиваем кнопку при наведении */
}

/* Эффект на активное состояние (при нажатии) */
.styled-button:active {
    transform: scale(1); /* Сбрасываем увеличение */
    box-shadow: 0 4px 8px rgba(0, 128, 0, 0.5); /* Уменьшаем тень */
}


/* Стили для кнопки "Предыдущая страница" */
.previos_page_button {
    position: absolute;
    top: 20px;
    right: 20px;
    background-color: white;
    color: #333;
    border: 2px solid #333;
    padding: 16px 32px;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    z-index: 1000;
}
.previos_page_button:hover {
    background-color: #f0f0f0;
    transform: scale(1.05);
}
.previos_page_button:active {
    transform: scale(1);
}
```

#### Код для `preview_all.css`:

```css

@media print {
    .print_button {
        display: none !important;
    }

    h1 {
        display: none;
    }

    @page {
        size: A4 portrait;
        margin: 5px;
    }

    /* Скрыть первую страницу */
    /* body > *:first-child {
        display: none !important;
    } */

    /* Скрыть последнюю страницу */
    /* body > *:last-child {
        display: none !important;
    } */

    .page-break {
        display: block;
        height: 0;
        page-break-before: always;
        page-break-after: always;
    }
}

.print_button {
background-color: #007BFF;
color: white;
padding: 12px 24px;
border: none;
border-radius: 8px;
font-size: 16px;
cursor: pointer;
margin-bottom: 20px;
transition: background-color 0.3s ease;
}

.print_button:hover {
background-color: #0056b3;
}

iframe {
    width: 100%;
    height: 1000px;
    border: none;
    margin-bottom: 40px;
    page-break-after: always;
}
body {
    margin: 0;
    padding: 20px;
    font-family: Arial, sans-serif;
}
```

#### Код для `print_foarm.css`:

```css
/* Стиль для печати и форматирование страницы A4 */
@page {
    size: A4 portrait;  /* или landscape при необходимости */
    margin: 2cm; /* Отступы по периметру страницы */
}

@media print {
    body {
        background: none !important;
        margin: 0;
        padding: 0;
    }

    * {
        box-shadow: none !important;
        background: none !important;
        color: black !important;
    }

    .container {
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        box-shadow: none !important;
        overflow: hidden;
        transform-origin: top left;
    }

    /* Скрыть всё вне .container */
    /* body > *:not(.container) {
        display: none !important;
    } */
}

/* Общие стили для содержимого страницы */
body {
    font-family: Times New Roman, Georgia, serif;
    background-color: rgb(248, 200, 124);
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
}
.container {    
    width: 50%;                                         /* Устанавливаем ширину контейнера на 50% от ширины родительского элемента */
    margin: 50px auto;                                  /* Автоматические отступы по бокам и 50px сверху и снизу, чтобы центрировать контейнер */    
    background-color: white;                          /* Устанавливаем белый фон для контейнера */    
    padding: 20px;                                      /* Внутренние отступы, чтобы текст не прилегал к краям контейнера */    
    border-radius: 8px;                                 /* Скругляем углы контейнера радиусом 8px */    
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);         /* Добавляем тень для контейнера, чтобы создать эффект "выпуклости" */
}
.header {
    text-align: right;
    font-size: 20px;
    font-weight: normal;
}
.top{
    position: relative; /* .top позиционируется относительно того места, где его "поставил" родитель — .header.*/
    top: 1px;   /* Отступ сверху */
    right: 80px; /* Отступ справа */
    /*bottom: 50px;*/
}
.inscriptions{
    position: relative;
    font-size: 14px;
    top: 5px;   /* Отступ сверху */
    right: 120px; /* Отступ справа */
}
.low {
    font-size: 0.8em;      /* Уменьшаем размер шрифта */
    color: #888;           /* Меняем цвет текста на светло-серый */
    font-style: italic;    /* Делаем текст курсивом */
}
.left-column {
    width: 50%; /* Задаем ширину для левой колонки */
}
.right-column {
    width: 50%; /* Задаем ширину для правой колонки */
    text-align: center; /* Центрирование текста в ячейке */
}

/* Содержание записки */
.content {
    position: relative;
    margin-top: 40px;
    font-size: 20px;
    margin-bottom: 40px;
    line-height: 1.5;
    width: 100%; /* Убедимся, что контейнер растягивается на 100% ширины */
    box-sizing: border-box; /* Чтобы padding не выходил за пределы контейнера */
}
.bold{
    font-weight: bold;
}
.center{
    text-align: center;  /* Центрируем текст по горизонтали */
    vertical-align: middle;  /* Центрируем текст по вертикали */
}
.left{
    text-align: left;  /* Центрируем текст по горизонтали */
    vertical-align: middle;  /* Центрируем текст по вертикали */
}

/* Стили для таблицы */
.table {
    width: 100%;    /* Таблица будет занимать всю ширину контейнера */
    border-collapse: collapse;  /* Убираем двойные границы */
    margin-bottom: 0;  /*Убираем отступы между таблицами */
    line-height: 1.5;
}
.table td {
    border: 2px solid black; /* Жирные границы таблицы */
    padding: 8px;
    /*text-align: left; /* Выравнивание текста в ячейках по умолчанию */
}

/* Стили для прозрачной таблицы */
.transparent-table {
    border-collapse: collapse;
    width: 100%;
    line-height: 1.5;
}
.transparent-table td, 
.transparent-table th {
    border: none;
    background: transparent;
    padding: 0;
    margin: 0;
    color: inherit; /* сохраняем цвет текста, если нужно */
}

/* Стили для подписи директора */
.boss_left_column {
    width: 33%; /* Задаем ширину для левой колонки */
}
.boss_right_column {
    width: 33%; /* Задаем ширину для левой колонки */
    text-align: center; /* Центрирование текста в ячейке */
}




/* Стили для кнопки "Просмотр и печать" */
.print_button {
    position: absolute;
    top: 20px;
    left: 20px;
    background-color: white;
    color: #333;
    border: 2px solid #333;
    padding: 16px 32px;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    z-index: 1000;
}
.print_button:hover {
    background-color: #f0f0f0;
    transform: scale(1.05);
}
.print_button:active {
    transform: scale(1);
}

/* Стили для кнопки "Следующая страница" */
.next_page_button {
    position: absolute;
    top: 20px;
    right: 20px;
    background-color: white;
    color: #333;
    border: 2px solid #333;
    padding: 16px 32px;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    z-index: 1000;
}
.next_page_button:hover {
    background-color: #f0f0f0;
    transform: scale(1.05);
}
.next_page_button:active {
    transform: scale(1);
}

/* Стили для кнопки "Предыдущая страница" */
.previos_page_button {
    position: absolute;
    top: 100px;
    right: 20px;
    background-color: white;
    color: #333;
    border: 2px solid #333;
    padding: 16px 32px;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    z-index: 1000;
}
.previos_page_button:hover {
    background-color: #f0f0f0;
    transform: scale(1.05);
}
.previos_page_button:active {
    transform: scale(1);
}
```

#### Код для `registry.css`:

```css
/* Основные стили */
body {
    font-family: Arial, sans-serif;
    background-color: #f4f7fb;  /* Светлый фон для контраста */
    margin: 0;
    padding: 0;
}

.container {
    width: 95%;
    max-width: 2000px;
    margin: 30px auto;
    background: #fff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* Заголовок страницы */
h1 {
    text-align: center;
    color: #333;
    margin-bottom: 20px;
}

/* Стиль для таблицы */
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th, td {
    border: 1px solid #ccc;
    padding: 12px 15px;
    text-align: left;
    font-size: 14px;
}

/* Стили для заголовков */
th {
    background-color: #007BFF;
    color: white;
}

/* Чередование фона строк */
tr:nth-child(even) {
    background-color: #f9f9f9;
}

/* Кнопки */
button {
    display: block;
    width: 100%;
    padding: 6px 12px;
    margin-bottom: 6px;
    font-size: 14px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    color: white;
    transition: background-color 0.2s ease;
}

button.approve {
    background-color: #28a745;
}

button.approve:hover {
    background-color: #218838;
}

button.reject {
    background-color: #dc3545;
}

button.reject:hover {
    background-color: #c82333;
}

/* Стили для текста */
p {
    font-size: 16px;
    color: #333;
}

/* Стиль для кнопки выхода */
.logout-button {
    padding: 5px 12px;
    background-color: #f44336; /* Красный фон кнопки */
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.2s ease; /* Плавное изменение цвета фона */
    text-align: center; /* Центрирование текста */
    min-width: 80px; /* Минимальная ширина кнопки */
    width: 120px;
}

.logout-button:hover {
    background-color: #d32f2f; /* Темный красный при наведении */
}

.logout-button:focus {
    outline: none; /* Убираем контур при фокусе */
}
```

#### Код для `report.css`:

```css
/* Стиль для печати и форматирование страницы A4 */
@page {
    size: A4 portrait;  /* или landscape при необходимости */
    margin: 2cm; /* Отступы по периметру страницы */
}

@media print {
    body {
        background: none !important;
        margin: 0;
        padding: 0;
    }

    * {
        box-shadow: none !important;
        background: none !important;
        color: black !important;
    }

    .container {
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        box-shadow: none !important;
        overflow: hidden;
        transform-origin: top left;
    }

    /* Скрыть всё вне .container */
    /* body > *:not(.container) {
        display: none !important;
    } */
}

/* Общие стили для содержимого страницы */
body {
    font-family: Times New Roman, Georgia, serif;
    background-color: rgb(248, 200, 124);
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
}
.container {    
    width: 50%;                                         /* Устанавливаем ширину контейнера на 50% от ширины родительского элемента */
    margin: 50px auto;                                  /* Автоматические отступы по бокам и 50px сверху и снизу, чтобы центрировать контейнер */    
    background-color: white;                          /* Устанавливаем белый фон для контейнера */    
    padding: 20px;                                       /* Внутренние отступы, чтобы текст не прилегал к краям контейнера */    
    border-radius: 8px;                                 /* Скругляем углы контейнера радиусом 8px */    
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);         /* Добавляем тень для контейнера, чтобы создать эффект "выпуклости" */
}
.top{
    position: relative;
    top: 1px;   /* Отступ сверху */
    right: 80px; /* Отступ справа */
    bottom: 50px;
}
.header {
    text-align: right;
    font-size: 20px;
    font-weight: normal;
}

.low {
    font-size: 0.8em;      /* Уменьшаем размер шрифта */
    color: #888;           /* Меняем цвет текста на светло-серый */
    font-style: italic;    /* Делаем текст курсивом */
}

/* Содержание записки */
.content {
    margin-top: 40px;
    margin-bottom: 40px;
    font-size: 16px;
    line-height: 1.5;
    width: 100%; /* Убедимся, что контейнер растягивается на 100% ширины */
    box-sizing: border-box; /* Чтобы padding не выходил за пределы контейнера */
}

/* Стили для таблицы */
.table {
    width: 100%;    /* Таблица будет занимать всю ширину контейнера */
    border-collapse: collapse;  /* Убираем двойные границы */
    line-height: 1;
}
.table td {
    border: 1px solid black; /* Жирные границы таблицы */
}

/* Стили для прозрачной таблицы */
.transparent-table {
    width: 100%;
    border-collapse: collapse;
    line-height: 1;
}
.transparent-table td, 
.transparent-table th {
    border: none;
}

.with-border {
    padding: 0px 0;
    border-bottom: 1px solid black;
}




/* Стили для кнопки "Просмотр и печать" */
.print_button {
    position: absolute;
    top: 20px;
    left: 20px;
    background-color: white;
    color: #333;
    border: 2px solid #333;
    padding: 16px 32px;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    z-index: 1000;
}
.print_button:hover {
    background-color: #f0f0f0;
    transform: scale(1.05);
}
.print_button:active {
    transform: scale(1);
}

/* Стили для кнопки "Следующая страница" */
.next_page_button {
    position: absolute;
    top: 20px;
    right: 20px;
    background-color: white;
    color: #333;
    border: 2px solid #333;
    padding: 16px 32px;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    z-index: 1000;
}
.next_page_button:hover {
    background-color: #f0f0f0;
    transform: scale(1.05);
}
.next_page_button:active {
    transform: scale(1);
}

/* Стили для кнопки "Предыдущая страница" */
.previos_page_button {
    position: absolute;
    top: 20px;
    right: 20px;
    background-color: white;
    color: #333;
    border: 2px solid #333;
    padding: 16px 32px;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    z-index: 1000;
}
.previos_page_button:hover {
    background-color: #f0f0f0;
    transform: scale(1.05);
}
.previos_page_button:active {
    transform: scale(1);
}
```

#### Код для `start_page.css`:

```css
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    margin: 0;
    padding: 0;
}

header {
    background-color: #4CAF50;
    color: white;
    padding: 20px;
    text-align: center;
}

main {
    padding: 20px;
}

h2 {
    font-size: 1.5em;
    color: #333;
}

footer {
    text-align: center;
    padding: 10px;
    background-color: #4CAF50;
    color: white;
    position: fixed;
    bottom: 0;
    width: 100%;
}

.admin-button {
    position: fixed;
    bottom: 80px; /* чуть выше футера */
    right: 30px;
    padding: 12px 20px;
    background-color: #2196F3;
    color: white;
    border: none;
    border-radius: 50px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    cursor: pointer;
    font-size: 16px;
    z-index: 1000;
    transition: background-color 0.3s ease, transform 0.2s ease;
}

.admin-button:hover {
    background-color: #1976D2;
    transform: scale(1.05);
}


/* Стили для кнопки "Перейти к заполнению данных" */
.form_button {
    background: linear-gradient(135deg, #6c63ff, #42a5f5);
    color: #fff;
    border: none;
    padding: 14px 28px;
    font-size: 17px;
    font-weight: 600;
    border-radius: 12px;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(108, 99, 255, 0.4);
    transition: background 0.3s ease, box-shadow 0.3s ease;
}

.form_button:hover {
    background: linear-gradient(135deg, #5a54e9, #3595e2);
    box-shadow: 0 6px 20px rgba(66, 165, 245, 0.5);
}

.form_button:active {
    box-shadow: 0 3px 8px rgba(66, 165, 245, 0.6);
}

/* Стили для контейнера формы авторизации */
.login-container {
    max-width: 350px;
    margin: 40px auto;
    padding: 20px 25px;
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.login-container h2 {
    text-align: center;
    margin-bottom: 20px;
    color: #333;
}

.login-container form {
    display: flex;
    flex-direction: column;
}

.login-container label {
    margin-bottom: 6px;
    color: #444;
    font-size: 14px;
}

.login-container input {
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 14px;
    transition: border 0.3s ease;
}

.login-container input:focus {
    border-color: #007bff;
    outline: none;
}

.login-container button {
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 15px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.login-container button:hover {
    background-color: #0056b3;
}
```

### Шаг 6: JavaScript для загрузки файлов


#### Код для `auth.js`:

```javascript
function login(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Простой вариант (для демо). Лучше на сервере.
    if (username === 'admin' && password === 'adminpft,fkb') {
        sessionStorage.setItem('auth', 'true');
        window.location.href = 'dashboard.html';
    } else {
        alert('Неверные данные');
    }
}

```

#### Код для `dashboard.js`:

```javascript
document.getElementById('copyFileBtn').addEventListener('click', function() {
    // Получаем базовый URL из текущего местоположения страницы
    const baseURL = window.location.origin;

    // Используем относительный путь, чтобы работать как на локальной версии, так и на сервере
    fetch(baseURL + '/copy-file', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Ошибка при копировании файла:', error);
    });
});

// Обработчик для кнопки перехода на страницу заполнения данных
document.getElementById('goToInputPage').addEventListener('click', function() {
    window.location.href = '/input'; // Перенаправление на страницу "/input"
});

//Обработчик для кнопки получения актуальных данных по сотрудникам
document.addEventListener("DOMContentLoaded", function () {
    const updateButton = document.getElementById("refreshEmployeeData");

    if (updateButton) {
        updateButton.addEventListener("click", function (e) {
            e.preventDefault();  // Предотвращаем стандартное поведение кнопки

            // Отправляем POST-запрос на сервер
            fetch('/update_employees', {
                method: 'POST'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Ошибка обновления данных");
                }
                return response.json();
            })
            .then(data => {
                // Показываем сообщение об успешной актуализации
                alert("✅ Список сотрудников обновлён");
            })
            .catch(error => {
                console.error("Ошибка:", error);
                alert("❌ Не удалось обновить список сотрудников");
            });
        });
    }
});
```

#### Код для `index.js`:

```javascript
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("loginForm");

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value;

        try {
            const response = await fetch("/api/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password })
            });

            const result = await response.json();

            if (result.success) {
                alert("Успешный вход!");
                // Перенаправление на нужную страницу:
                window.location.href = "/input";
            } else {
                alert(result.message || "Ошибка входа.");
            }
        } catch (error) {
            alert("Ошибка соединения с сервером.");
            console.error(error);
        }
    });
});
```

#### Код для `input.js`:

```javascript
// Добавление поля для представителей организации
document.getElementById('addOrgRep').addEventListener('click', function() {
    const newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.name = 'orgRepresentatives[]';
    document.getElementById('orgRepresentatives').appendChild(newInput);
});

// Добавление поля для представителей АО "ИнфоТеКС"
document.getElementById('addInfotexRep').addEventListener('click', function() {
    const newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.name = 'infotexRepresentatives[]';
    document.getElementById('infotexRepresentatives').appendChild(newInput);
});

// Добавление поля для представителей АО «ПМ»
document.getElementById('addPmRep').addEventListener('click', function() {
    const newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.name = 'pmRepresentatives[]';
    document.getElementById('pmRepresentatives').appendChild(newInput);
});

// Перенос ФИО сотрудника в первую графу ФИО представителей АО «ПМ»
document.addEventListener('DOMContentLoaded', function () {
    const employeeNameInput = document.getElementById('employeeName');
    const pmRepContainer = document.getElementById('pmRepresentatives');
    const addPmRepButton = document.getElementById('addPmRep');
    let firstPmInput = pmRepContainer.querySelector('input'); // Изначально первое поле для представителей

    // Слушаем событие ввода текста в поле "ФИО сотрудника"
    employeeNameInput.addEventListener('input', function () {
        // Если первое поле для представителей существует
        if (firstPmInput) {
            // Обновляем значение первого поля в "pmRepresentatives" с тем, что введено в поле "employeeName"
            firstPmInput.value = employeeNameInput.value;
        }
    });
});

// Проверка и заполнение данных по сотрудникам организации
function checkEmployee() {
    const employeeName = document.getElementById("employeeName").value.trim();  // Получаем значение из поля ввода, убираем лишние пробелы

    if (!employeeName || employeeName.length < 5) { // Если поле пустое или слишком короткое — сразу очищаем связанные поля и выходим
        document.getElementById("position").value = '';
        document.getElementById("branch").value = '';
        document.getElementById("department").value = '';
        return;
    }

    fetch('/check_employee', {  // Отправляем POST-запрос на серверный маршрут /check_employee
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'  // Сообщаем, что отправляем JSON
        },
        body: JSON.stringify({ employeeName: employeeName })    // Само тело запроса: имя сотрудника
    })
    .then(response => {
        if (!response.ok) { // Если ответ НЕ успешный (например, 404), значит сотрудник не найден
            document.getElementById("position").value = ''; // Очищаем поля должности и подразделения
            document.getElementById("branch").value = '';
            document.getElementById("department").value = '';
            throw new Error('Сотрудник не найден'); // Генерируем исключение, чтобы перейти к .catch()
        }
        return response.json(); // Если всё в порядке — преобразуем JSON-ответ в объект
    })
    .then(data => {
        if (data.status === 'found') {  // Если в ответе есть статус "found", заполняем нужные поля
            document.getElementById("position").value = data.data.position;
            document.getElementById("branch").value = data.data.branch;
            document.getElementById("department").value = data.data.department;
        }
    })
    .catch(error => {
        console.warn('Ошибка при получении данных о сотруднике:', error);   // Обработка ошибки — выводим её в консоль
    });
}

// Навешиваем обработчик после полной загрузки DOM
document.addEventListener("DOMContentLoaded", function () { // Когда страница полностью загружена (весь HTML доступен)
    const employeeInput = document.getElementById("employeeName");  // Получаем ссылку на поле ввода ФИО сотрудника

    let debounceTimeout;    // Создаём переменную для хранения задержки (таймера)
    employeeInput.addEventListener("input", function () {   // Добавляем обработчик события "input" — он срабатывает при любом изменении поля
        clearTimeout(debounceTimeout);  // Удаляем предыдущий таймер (если пользователь продолжает печатать)
        debounceTimeout = setTimeout(checkEmployee, 400); // Устанавливаем новый таймер: вызовем функцию только через 400 мс после последнего ввода
    });
});
```

#### Код для `print_form.js`:

```javascript
// Извлечение данных из URL
document.getElementById('note-number').innerText = generateNoteNumber();
document.getElementById('event_date').innerText = generateDateString(5);
document.getElementById('employee_name').innerText = 'Иванов И. И.';  // Пример
document.getElementById('organization-name').innerText = 'ООО «Компания»';  // Пример
document.getElementById('meeting-purpose').innerText = 'Обсуждение условий сотрудничества а что если текста будет чутбла бла блабла бла блабла бла блабла бла блабла бла блабла бла блабла бла блабла бла блаь больше чем надо для проверки растяжения страницы бла бла блабла бла блабла бла блабла бла блабла бла блабла бла блабла бла блабла бла блабла бла бла';  // Пример
document.getElementById('expenses').innerText = '1 000,00';  // Пример

// Функция для вычисления даты на 5 дней раньше текущей
function generateDateString(daysBefore) {
    const today = new Date();
    today.setDate(today.getDate() - daysBefore);
    return today.toLocaleDateString('ru-RU');
}

// Функция для формирования номера служебной записки
function generateNoteNumber() {
    const date = new Date();
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate() - 5).padStart(2, '0');  // 5 дней назад
    return `${year}${month}${day}-1`;
        }
```

#### Код для `registry.js`:

```javascript
function approveEntry(index) {
    console.log(`Отправляем запрос на согласование записи с индексом: ${index}`);
    console.log(`Роль: ${userRole}`);
    
    // Отправка запроса на сервер
    fetch(`/api/registry/approve/${index}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ role: userRole })  // Передаем роль пользователя
    })
    .then(response => response.json())
    .then(data => {
        console.log('Ответ от сервера:', data);

        // Обновляем статус записи в таблице, не перезагружая страницу
        const approvedCell = document.getElementById(`approved-cell-${index}`);
        if (approvedCell) {
            if (userRole === 'neiger') {
                approvedCell.innerHTML = 'Согласовано Нейгером';
            } else {
                approvedCell.innerHTML = 'Согласовано';
            }
        }
    })
    .catch(error => {
        console.error('Ошибка при запросе:', error);
    });
}

function rejectEntry(index) {
    fetch(`/api/registry/reject/${index}`, { method: 'POST' })
        .then(() => location.reload());
}

function deleteEntry(index) {
    fetch(`/api/registry/delete/${index}`, { method: 'POST' })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert("Ошибка при удалении записи");
            }
        });
}

function logout() {
    fetch('/logout', { method: 'GET' }).then(() => {
        window.location.href = "/";
    });
}
```

### Шаг 7: Запустите Flask сервер
Теперь, когда все файлы созданы, перейдите в каталог проекта и запустите сервер Flask:

```bash
python app.py
```

Если все сделано правильно, сервер будет работать на `http://127.0.0.1:5000/`.

### Шаг 8: Тестирование
1. Перейдите по адресу `http://127.0.0.1:5000/` в браузере.
2. Убедитесь, что сайт работает.

### Дополнительные шаги:
- Убедитесь, что у вас есть необходимые права доступа для работы с файлами на сервере, особенно если вы работаете с каталогами типа `/var/www/`.

# Для активации default добавьте символическую ссылку:
```bash
sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/
sudo systemctl reload nginx
sudo systemctl restart nginx
```

# Исправление ошибок

Проверьте, что Flask-приложение запущено
Убедитесь, что ваше Flask-приложение действительно запущено и работает на порту 5000. Вы можете проверить это с помощью команды:

```bash
sudo netstat -tuln | grep 5000
```
Если вы не увидите строки с `127.0.0.1:5000` или `0.0.0.0:5000`, значит Flask не слушает на этом порту.

Проверьте настройки Nginx
Убедитесь, что конфигурация Nginx правильная и Nginx работает. Проверьте, что Nginx настроен на прослушивание порта 80:

```bash
sudo netstat -tuln | grep :80
```
Если вы не видите строку с `0.0.0.0:80` или `10.121.1.164:80`, значит Nginx не прослушивает порт 80. В этом случае, перезапустите Nginx:

```bash
sudo systemctl restart nginx
```
Системный статус через systemd
```bash
systemctl status nginx
```

**Узнать, кто использует порт**

```bash
sudo lsof -i :80
```
**lsof** = **LiSt Open Files**

**Остановить локальный nginx на хосте**

```bash
sudo systemctl stop nginx
```




---

# Разворачиваем Flask-сервер на хостовой машине (Windows), в папке `D:\Git\flask_server`.

---

### 🔧 Шаг 1. Создаём виртуальное окружение

Открой PowerShell **в этой папке**:

```powershell
cd D:\Git\flask_server
```
---

### Шаг 2. Изменение политики выполнения скриптов
Открой PowerShell от имени администратора и выполни следующую команду:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Эта команда разрешит запуск локальных скриптов и скриптов, загруженных из интернета, если они подписаны. Подтверди командой `Y`.

```powershell
python -m venv venv
C:\Users\Kovalenko.Kon\AppData\Local\Programs\Python\Python312\python.exe -m venv venv
```

---

### ▶️ Шаг 3. Активируем окружение

```powershell
.\venv\Scripts\activate
```

Если всё ок, в начале строки будет `(venv)`.

---

### 📦 Шаг 4. Устанавливаем Flask

```powershell
pip install flask
pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org flask
C:\Users\Kovalenko.Kon\AppData\Local\Programs\Python\Python312\python.exe -m pip install --upgrade pip --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
```

---

### 📝 Шаг 5. Создаём файл `app.py`

Создай файл `app.py` в той же папке со следующим содержимым:

```python
from flask import Flask, jsonify, request
import pyodbc
import json

app = Flask(__name__)

# Параметры подключения к MSSQL
mssql_conn_params = {
    'driver': '{ODBC Driver 17 for SQL Server}',
    'server': 'msk-sql-02',
    'database': 'RKM',
    'uid': 'rkm',
    'pwd': 'UF5rrXp49IgA1$f6'
}

@app.route('/employee-changes')
def get_employee_changes():
    # Получаем параметр "limit" из запроса, если он существует
    limit = request.args.get('limit', default=None, type=int)

    try:
        # Строка подключения
        conn_str = (
            f"DRIVER={mssql_conn_params['driver']};"
            f"SERVER={mssql_conn_params['server']};"
            f"DATABASE={mssql_conn_params['database']};"
            f"UID={mssql_conn_params['uid']};"
            f"PWD={mssql_conn_params['pwd']}"
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Выполнение хранимой процедуры
        cursor.execute("EXEC EmployeeChanges_v_1_6")
        rows = cursor.fetchall()

        # Преобразуем результат в список словарей
        result = []
        for i, row in enumerate(rows):  # Используем i для отслеживания количества
            # Не декодируем значения - оставляем как есть
            name = row[0]
            position = row[1]
            department = row[2]
            branch = row[3]

            result.append({
                "name": name,
                "position": position,
                "department": department,
                "branch": branch
            })

            # Если ограничение по количеству записей задано, выходим из цикла
            if limit is not None and i >= limit - 1:
                break

        # Отправляем ответ в корректном формате
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

---

### 🧪 Шаг 6. Запускаем сервер

```powershell
python app.py
```

Если всё ок, увидишь:

```
 * Running on http://127.0.0.1:5000/
```

---

### 🌐 Шаг 7. Проверка с Linux-сервера

На Linux-сервере (где Flask не видит БД) выполни:

```bash
curl http://10.121.1.40:5000/employee-changes
```

Если всё работает, сервер отдаст JSON-ответ.


### Шаг 8. Установка библиотеки pyodbc в виртуальное окружение:

```bash
pip install pyodbc
pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org pyodbc
```

### Шаг 9. Проверка API

После того как Flask сервер запустится, вы сможете получить данные, сделав HTTP GET запрос к /employee-changes, например, с помощью curl:

```bash
curl http://10.121.1.40:8080/employee-changes
curl --noproxy '*' http://10.121.1.40:8080/employee-changes
```

### Шаг 10. Даем всем права на запись в файл:

```bash
sudo chmod 666 /var/www/local.work/data/employee.json
```
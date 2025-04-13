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
pip list
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
    /html
        /shared
            Представительские.xlsb  <--- Файл доступный для скачивания всем
    /local.work
        /admin                  <--- Админский блок
            dashboard.html
            login.html
        /images
            background.png          <--- Картинки фона
            background2.png         <--- Картинки фона
        /static
            /css
                auth.css
                dashboard.scc
                start_page.css
            /js
                auth.js
        /templates
            index.html
        app.py
        _index.html         <--- Первоначальная ссылка на которой работал nginx
        reserv.copy.html    <--- Резервная копия index.html
        _style.css          <--- старые стили
    /logs
        access.log
        error.log        
    /settings
        default         <--- Жёсткие ссылки на конфиги nginx
        local.work      <--- Жёсткие ссылки на конфиги nginx
        nginx.conf      <--- Жёсткие ссылки на конфиги nginx
    /shared             <--- Общая директория между VM и хостом
        template.xlsb
    /venv
    
```

# 3: Создайте файл Flask-приложения (app.py)
Теперь создадим файл `app.py`, который будет сервером Flask. 

# Код для `app.py`:

```python
from flask import Flask, render_template, send_from_directory, request
import shutil
import os

app = Flask(__name__, static_folder='local.work', template_folder='local.work')

TEMPLATE_FILE = '/www/shared/template.xlsb'
DEST_FILE = '/www/html/shared/Представительские.xlsb'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/copy-file', methods=['POST'])
def copy_file():
    try:
        # Копируем файл с заменой
        shutil.copy(TEMPLATE_FILE, DEST_FILE)
        return "Файл успешно скопирован и заменен!"
    except Exception as e:
        return f"Ошибка при копировании файла: {e}"


if __name__ == '__main__':
    app.run(debug=True)
```

### Шаг 4: Создайте HTML страницу (index.html)
Теперь обновим ваш HTML файл для добавления кнопки для копирования файла. Мы добавим вторую кнопку и обработчик на стороне клиента (JavaScript), который будет отправлять запрос на сервер.

#### Код для `index.html`:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Управление файлами</title>
    <link rel="stylesheet" href="style.css">
    
    <style>
        /* Фон для этой страницы */
        body {
            background-image: url("/static/images/background.png");
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            height: 100vh;
            margin: 0;
            padding: 0;
        }
    </style>
</head>
<body>
    <h2>Загрузка файлов</h2>
    <form id="uploadForm" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <button type="submit">Загрузить</button>
    </form>

    <h3>Загруженные файлы</h3>
    <ul id="fileList"></ul>

    <h3>Копировать файл с заменой</h3>
    <button id="copyFileButton">Копировать файл</button>
    
    <script src="upload.js"></script>
    <script>
        document.getElementById('copyFileButton').addEventListener('click', function() {
            fetch('/copy-file', {
                method: 'POST'
            })
            .then(response => response.text())
            .then(data => {
                alert(data);  // Выведем сообщение о результате операции
            })
            .catch(error => {
                alert('Ошибка при копировании файла: ' + error);
            });
        });
    </script>
</body>
</html>
```

### Шаг 5: Создайте файл стилей (style.css)
Ваш CSS файл может остаться простым, если в нем не нужно ничего особо менять. Просто для оформления страницы.

#### Код для `style.css`:

```css
body {
    font-family: Arial, sans-serif;
    color: white;
    text-align: center;
}

h2 {
    color: #fff;
}

button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    border: none;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}
```

### Шаг 6: Напишите JavaScript для загрузки файла (upload.js)
Загрузку файлов можно оставить для дальнейшей доработки, но для примера, вот такой файл:

#### Код для `upload.js`:

```javascript
document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    let formData = new FormData(this);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert('Файл загружен: ' + data.filename);
    })
    .catch(error => {
        alert('Ошибка при загрузке файла: ' + error);
    });
});
```

### Шаг 7: Запустите Flask сервер
Теперь, когда все файлы созданы, перейдите в каталог проекта и запустите сервер Flask:

```bash
python app.py
```

Если все сделано правильно, сервер будет работать на `http://127.0.0.1:5000/`.

### Шаг 8: Тестирование
1. Перейдите по адресу `http://127.0.0.1:5000/` в браузере.
2. Убедитесь, что кнопка "Копировать файл" работает. При нажатии на нее файл должен быть скопирован и заменен.

### Дополнительные шаги:
- Для обработки загрузки файла вы можете создать отдельный маршрут в `app.py` и добавить функционал на клиентскую сторону.
- Убедитесь, что у вас есть необходимые права доступа для работы с файлами на сервере, особенно если вы работаете с каталогами типа `/var/www/`.

Таким образом, у вас будет настроено Flask-приложение, которое может копировать файл с одного места в другое по запросу.

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
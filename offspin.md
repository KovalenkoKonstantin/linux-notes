Для создания сайта с использованием Nginx на Ubuntu в VirtualBox, который будет доступен по адресу `local.work`, и с возможностью скачивания файла из каталога, а также для того, чтобы сайт был функциональным, выполним несколько шагов:

### 1. Установка Nginx

В терминале вашей виртуальной машины установите Nginx, используя следующие команды:

```bash
sudo apt update -y
sudo apt install -y nginx
```

Запустите Nginx и убедитесь, что он работает:

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```
Проверка статуса службы Nginx
```bash
sudo systemctl status nginx
```

Чтобы проверить, что Nginx работает, откройте браузер и перейдите по адресу `http://10.121.1.164`. Должна появиться стандартная страница **Nginx**.

### 2. Настройка домена `local.work`

Для того чтобы сайт был доступен по адресу `local.work`, вам нужно настроить виртуальный хост для **Nginx** и добавить запись в файл `hosts` на вашей системе.

#### 2.1 Настройка записи в файле `hosts`

Добавьте следующую строку в файл `/etc/hosts` на хосте (не внутри виртуальной машины)
но и на VM тоже можно добавить для работы сайта как текста:

```bash
sudo nano /etc/hosts
```
```bash
10.121.1.164 local.work
```

Это позволит вашему компьютеру резолвить домен `local.work` в IP-адрес виртуальной машины.

#### 2.2 Настройка Nginx для использования `local.work`

Создайте файл конфигурации для вашего сайта в директории `/etc/nginx/sites-available/` и создайте символическую ссылку в `/etc/nginx/sites-enabled/`:

```bash
sudo nano /etc/nginx/sites-available/local.work
```

Добавьте в файл следующий код:

```nginx
server {
    listen 80;
    server_name local.work;

    root /var/www/local.work;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }

    location /shared/ {
        alias /var/www/shared/;
        autoindex on;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.3-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

Удалите символическую ссылку на default (она ведёт к /var/www/html):

```bash
sudo rm /etc/nginx/sites-enabled/default
```

Теперь создайте символическую ссылку для включения сайта:

```bash
sudo ln -s /etc/nginx/sites-available/local.work /etc/nginx/sites-enabled/
```
#### 2.3 Установить PHP и модуль FPM
Установи PHP и FPM:

```bash
sudo apt update -y
sudo apt install php php-fpm
```

Убедись, что сокет /run/php/php8.1-fpm.sock существует:

```bash
ls /run/php/
```

#### 2.4 Перезапуск Nginx

Перезапустите Nginx, чтобы изменения вступили в силу:

```bash
sudo systemctl restart nginx
```

Какая-то фигня с кешем - помогает только ребут
```bash
sudo reboot
```


### 3. Создание структуры файлов

#### 3.1 Размещение сайта

Создайте директорию для вашего сайта:

```bash
sudo mkdir -p /var/www/local.work
```

Создайте файл `index.html` в директории `/var/www/local.work/` с простым содержимым:

```bash
sudo nano /var/www/local.work/index.html
```

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local Work</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>Добро пожаловать на сайт Local Work</h1>
    </header>
    <main>
        <section>
            <h2>Скачать файл</h2>
            <p>Нажмите на ссылку, чтобы скачать файл <a href="/shared/template.xlsb" download>template.xlsb</a>.</p>
        </section>
    </main>
    <footer>
        <p>&copy; 2025 Local Work</p>
    </footer>
</body>
</html>
```

#### 3.2 Добавление стилей

Создайте файл `styles.css` в той же директории с базовыми стилями для сайта:

```bash
sudo nano /var/www/local.work/styles.css
```

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
```

#### 3.3 Расшаривание каталога

Теперь создайте каталог для расшаривания файла:

```bash
sudo mkdir -p /var/www/shared
```

Выключить VM и создать `shared` каталог через настройки VM.

Добавить `www-data` (**Nginx** работает от имени **www-data**) в группу `vboxsf`, чтобы он  получил доступ к `shared`:

```bash
sudo usermod -aG vboxsf www-data
```
Затем обязательно перегружаем ВМ, чтобы изменения применились:
```bash
sudo reboot
```
#### 3.4 Указание корневого пути nginx
Cтандартный путь по умолчанию для веб-директории в `Ubuntu` при установке `nginx` или `Apache`. есть:

в конфиге:
```bash
sudo nano /etc/nginx/sites-available/default
```
обычно указано:

```bash
root /var/www/html;
```

Если не хочешь возиться с группами и перезагрузками, просто скопируй файл из общей папки в обычную директорию, которую nginx точно видит:

```bash
sudo mkdir -p /var/www/html/shared
sudo cp /var/www/shared/template.xlsb /var/www/html/shared/
sudo chown www-data:www-data /var/www/html/shared/template.xlsb
sudo chown www-data:www-data /var/www/html/shared/Представительские.xlsb
sudo chmod 644 /var/www/html/shared/template.xlsb
sudo chmod 644 /var/www/html/shared/Представительские.xlsb
sudo chmod o+rx /var/www/html/shared
sudo chmod o+r /var/www/html/shared/template.xlsb
sudo chmod o+r /var/www/html/shared/Представительские.xlsb
```
`-p` — означает: "создавать родительские папки, если их нет", и не выдавать ошибку, если папка уже существует.
`chown` = **change owner** — изменить владельца файла.
`644` — это набор прав в числовом виде:
* **6** → для владельца (user): `read + write` = `4 + 2`
* **4** → для группы: `read`
* **4** → для остальных: `read`

Проверь права на папку и файл
```bash
ls -ld /var/www/html/shared
ls -l /var/www/html/shared/Представительские.xlsb
ls -l /var/www/html/shared/template.xlsb
```

Полная перезагрузка (на всякий случай):

```bash
sudo systemctl restart nginx
```
Чтобы убедиться, что не допущена ошибка в конфиге:

```bash
sudo nginx -t
```
```bash
sudo reboot
```

#### 3.5 Дать доступ "всем" (просто и быстро)
```bash
sudo chmod o+rx /var/www/shared
sudo chmod o+rx /var/www/local.work/images
sudo chmod o+r /var/www/local.work/images/background.png
sudo chmod o+rx /var/www/local.work
```

#### 3.6. Для диагностики и возможного исправления проблемы можно временно отключить использование `sendfile()` в конфигурации `nginx`.

Открой конфигурацию nginx:

```bash
sudo nano /etc/nginx/nginx.conf
```
В секции `http` добавь или измените строку:

```bash
sendfile off;
```

### 4. Добавим кнопку внизу

```html
<!-- Вставить в конец <main> перед </main> -->
<section>
    <button onclick="location.href='/admin/login.html'">Перейти в режим администратора</button>
</section>
```

---

### ✅ 2. Файловая структура

Рекомендуемая структура:

```
/var/www/html/
├── index.html
├── styles.css
├── shared/
│   └── Представительские.xlsb
├── admin/
│   ├── login.html
│   ├── dashboard.html
│   ├── upload.js
│   ├── style.css
│   └── auth.js
```

---

### ✅ 3. login.html — Страница авторизации

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Авторизация</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h2>Вход администратора</h2>
    <form onsubmit="return login(event)">
        <label for="username">Логин:</label>
        <input type="text" id="username" required><br>
        <label for="password">Пароль:</label>
        <input type="password" id="password" required><br>
        <button type="submit">Войти</button>
    </form>
    <script src="auth.js"></script>
</body>
</html>
```

---

### ✅ 4. auth.js — Простой механизм авторизации (на клиенте)

```javascript
function login(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Простой вариант (для демо). Лучше на сервере.
    if (username === 'admin' && password === '1234') {
        sessionStorage.setItem('auth', 'true');
        window.location.href = 'dashboard.html';
    } else {
        alert('Неверные данные');
    }
}
```

---

### ✅ 5. dashboard.html — Страница загрузки и выбора основного файла

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Управление файлами</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h2>Загрузка файлов</h2>
    <form id="uploadForm" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <button type="submit">Загрузить</button>
    </form>

    <h3>Загруженные файлы</h3>
    <ul id="fileList"></ul>

    <script src="upload.js"></script>
</body>
</html>
```

---

### ✅ 6. upload.js — Скрипт загрузки и управления

> Здесь предполагается, что сервер поддерживает POST и копирование файлов через `cgi`, `php`, `Flask`, `Node.js`, etc. Пример — позже.

```javascript
window.onload = function() {
    if (sessionStorage.getItem('auth') !== 'true') {
        window.location.href = 'login.html';
        return;
    }

    loadFiles();

    document.getElementById('uploadForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(this);

        fetch('/upload.php', {
            method: 'POST',
            body: formData
        }).then(res => res.text()).then(data => {
            alert(data);
            loadFiles();
        });
    });
};

function loadFiles() {
    fetch('/list-files')
        .then(response => response.json())
        .then(files => {
            const ul = document.getElementById('fileList');
            ul.innerHTML = '';
            files.forEach(file => {
                const li = document.createElement('li');
                li.innerHTML = `
                    ${file}
                    <button onclick="setMainFile('${file}')">Сделать основным</button>
                `;
                ul.appendChild(li);
            });
        });
}

function setMainFile(filename) {
    fetch('/set-main', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ filename })
    }).then(res => res.text()).then(alert);
}
```

---

### ✅ 7. upload.php

```php
<?php
$uploadDir = __DIR__ . '/upload/';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
    $fileName = basename($_FILES['file']['name']);
    $destination = $uploadDir . $fileName;

    if (move_uploaded_file($_FILES['file']['tmp_name'], $destination)) {
        echo "Файл успешно загружен.";
    } else {
        http_response_code(500);
        echo "Ошибка при сохранении файла.";
    }
} else {
    http_response_code(400);
    echo "Неверный запрос.";
}
?>
```
✅ **Проверь права доступа**
Убедись, что `nginx` имеет доступ на запись в папку `upload`:

```bash
sudo chown -R www-data:www-data /var/www/local.work/admin/upload
sudo chmod -R 755 /var/www/local.work/admin/upload
```

### ✅ Да, можно и даже **нужно**, если ты хочешь отслеживать активность на локальном сайте. Учитывая, что у тебя установлен **Nginx**, основную часть логирования можно сделать через его встроенные механизмы. Вот как это можно реализовать:

---

## 🔧 **Логирование IP, времени и URL (в т.ч. скачивания)**

В файле конфигурации nginx (обычно это `/etc/nginx/nginx.conf` или `/etc/nginx/sites-available/default`) ты можешь настроить формат логов.

### ✅ Пример кастомного лог-формата:

```nginx
log_format download_log '$remote_addr - $remote_user [$time_local] '
                        '"$request" $status $body_bytes_sent '
                        '"$http_referer" "$http_user_agent"';
```

Это создаст лог, где будет:
- IP пользователя
- время запроса
- какой URL он запрашивал (`$request`)
- статус (например `200` или `404`)
- с какого ресурса перешёл (если был переход)
- юзер-агент (браузер/устройство)

### 🔽 Пример записи в лог:

```nginx
access_log /var/log/nginx/access.log download_log;
```

---

## 🧾 2. **Анализ скачиваний файла**

Чтобы отследить именно скачивания `Представительские.xlsb`, можно:

### Вариант 1: **Фильтровать лог по URL**

```bash
grep 'Представительские.xlsb' /var/log/nginx/access.log
```

Ты увидишь все обращения к этому файлу, включая IP, дату и время.

### Вариант 2: **Выделить скачивания в отдельный лог**

В конфиге Nginx можно выделить локацию:

```nginx
location /shared/Представительские.xlsb {
    access_log /var/log/nginx/downloads.log download_log;
    root /path/to/your/site;
}
```

Так ты сможешь отдельно отслеживать все скачивания, не мешая их с общим доступом ко всему сайту.

---

## 🧠 Бонус: Подсчёт скачиваний

Можно использовать простую команду:

```bash
cat /var/log/nginx/downloads.log | wc -l
```

Чтобы узнать, сколько раз файл был скачан.

---

## 💡 Альтернатива — JS + серверная статистика

Можно ещё отслеживать клики через JS + отправку на backend, но если тебе просто нужно знать **факт скачивания**, достаточно nginx.

---

Если хочешь — могу помочь тебе составить готовый фрагмент конфигурации nginx под твой сайт. Напиши, как у тебя сейчас настроены блоки `server` и `location`.
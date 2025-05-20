Ниже — 🔥 **конспект по 30 ключевым директивам NGINX**, без которых не обойтись. Упор на практику, ясность, структуру. Подойдёт и для запоминания, и для реальной работы.

---

# 📘 Конспект: Основные директивы NGINX (ТОП-30)

| №   | Директива            | Контекст                     | Описание и пример                                                                                 |
| --- | -------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------- |
| 1️⃣ | `worker_processes`   | `main`                       | Кол-во воркеров (потоков обработки). Обычно = числу ядер.<br>💡 `worker_processes auto;`          |
| 2️⃣ | `worker_connections` | `events`                     | Макс. число соединений на воркер. <br>💡 `worker_connections 1024;`                               |
| 3️⃣ | `events`             | `main`                       | Блок настроек сетевых событий. <br>💡 `events { worker_connections 1024; }`                       |
| 4️⃣ | `http`               | `main`                       | Основной блок HTTP-настроек. <br>💡 `http { include mime.types; ... }`                            |
| 5️⃣ | `server`             | `http`                       | Виртуальный хост. <br>💡 `server { listen 80; server_name example.com; }`                         |
| 6️⃣ | `listen`             | `server`                     | Порт/интерфейс, который слушает сервер. <br>💡 `listen 80;` или `listen [::]:443 ssl;`            |
| 7️⃣ | `server_name`        | `server`                     | Имена хоста (доменов), которые обрабатывает блок. <br>💡 `server_name mysite.com www.mysite.com;` |
| 8️⃣ | `location`           | `server`, `location`         | Условие маршрутизации запросов. <br>💡 `location /images/ { ... }`                                |
| 9️⃣ | `root`               | `http`, `server`, `location` | Путь к файлам для ответа. <br>💡 `root /var/www/html;`                                            |
| 🔟  | `index`              | `http`, `server`, `location` | Главная страница директории. <br>💡 `index index.html index.htm;`                                 |

---

## 📡 Прокси и балансировка

| №      | Директива          | Контекст             | Описание и пример                                                                    |
| ------ | ------------------ | -------------------- | ------------------------------------------------------------------------------------ |
| 1️⃣1️⃣ | `proxy_pass`       | `location`           | Перенаправление запроса на бэкенд. <br>💡 `proxy_pass http://127.0.0.1:5000;`        |
| 1️⃣2️⃣ | `proxy_set_header` | `location`, `server` | Передача/подмена заголовков. <br>💡 `proxy_set_header Host $host;`                   |
| 1️⃣3️⃣ | `upstream`         | `http`               | Группа бэкендов (балансировка). <br>💡 `upstream backend { server 127.0.0.1:5000; }` |
| 1️⃣4️⃣ | `include`          | любой                | Подключение файла. <br>💡 `include /etc/nginx/conf.d/*.conf;`                        |
| 1️⃣5️⃣ | `try_files`        | `location`           | Проверка существования файлов. <br>💡 `try_files $uri $uri/ =404;`                   |

---

## 🔐 Безопасность и HTTPS

| №      | Директива             | Контекст                     | Описание и пример                                                               |
| ------ | --------------------- | ---------------------------- | ------------------------------------------------------------------------------- |
| 1️⃣6️⃣ | `ssl_certificate`     | `server`                     | Путь к сертификату. <br>💡 `ssl_certificate /etc/ssl/cert.pem;`                 |
| 1️⃣7️⃣ | `ssl_certificate_key` | `server`                     | Путь к приватному ключу.                                                        |
| 1️⃣8️⃣ | `ssl_protocols`       | `http`, `server`             | Разрешённые версии SSL/TLS. <br>💡 `ssl_protocols TLSv1.2 TLSv1.3;`             |
| 1️⃣9️⃣ | `ssl_ciphers`         | `http`, `server`             | Разрешённые шифры. <br>💡 `ssl_ciphers HIGH:!aNULL:!MD5;`                       |
| 2️⃣0️⃣ | `add_header`          | `http`, `server`, `location` | Добавление заголовков безопасности. <br>💡 `add_header X-Frame-Options "DENY";` |

---

## 📊 Логи и отладка

| №      | Директива    | Контекст                     | Описание и пример                                                                              |
| ------ | ------------ | ---------------------------- | ---------------------------------------------------------------------------------------------- |
| 2️⃣1️⃣ | `access_log` | `http`, `server`, `location` | Путь и формат лога доступа. <br>💡 `access_log off` `/var/log/nginx/access.log;`                     |
| 2️⃣2️⃣ | `error_log`  | `main`, `http`, `server`     | Путь и уровень логов ошибок. <br>💡 `error_log off` `/var/log/nginx/error.log warn;`                 |
| 2️⃣3️⃣ | `log_format` | `http`                       | Формат записи логов. <br>💡 `log_format main '$remote_addr - $remote_user [$time_local] ...';` |

---

## ⚙️ Управление поведением

| №      | Директива              | Контекст                     | Описание и пример                                                                              |
| ------ | ---------------------- | ---------------------------- | ---------------------------------------------------------------------------------------------- |
| 2️⃣4️⃣ | `client_max_body_size` | `http`, `server`, `location` | Максимальный размер запроса. <br>💡 `client_max_body_size 10M;`                                |
| 2️⃣5️⃣ | `keepalive_timeout`    | `http`, `server`, `location` | Время жизни соединения. <br>💡 `keepalive_timeout 65;`                                         |
| 2️⃣6️⃣ | `sendfile`             | `http`, `server`, `location` | Быстрая передача файлов ядром. <br>💡 `sendfile on;`                                           |
| 2️⃣7️⃣ | `gzip`                 | `http`, `server`, `location` | Включение gzip-сжатия. <br>💡 `gzip on;`                                                       |
| 2️⃣8️⃣ | `rewrite`              | `server`, `location`         | Переписывание URL. <br>💡 `rewrite ^/old$ /new permanent;`                                     |
| 2️⃣9️⃣ | `return`               | `server`, `location`         | Простое перенаправление или возврат кода. <br>💡 `return 301 https://example.com$request_uri;` |
| 3️⃣0️⃣ | `error_page`           | `http`, `server`, `location` | Пользовательские страницы ошибок. <br>💡 `error_page 404 /404.html;`                           |

---

# 🎁 Бонус: 💡 Типовые конструкции

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    error_page 404 /404.html;
    location = /404.html {
        root /var/www/html;
    }
}
```


таблица с **топ-50 директивами NGINX**, с пояснениями и примерами

---

### 📘 **Таблица: Топ-50 директив NGINX**

| №  | Директива              | Контекст               | Описание и пример                                               |
| -- | ---------------------- | ---------------------- | --------------------------------------------------------------- |
| 1  | `worker_processes`     | main                   | Кол-во рабочих процессов. `worker_processes auto;`              |
| 2  | `worker_connections`   | events                 | Макс. соединений на воркер. `worker_connections 1024;`          |
| 3  | `events {}`            | main                   | Блок для директив событий (например, `worker_connections`)      |
| 4  | `http {}`              | main                   | Основной блок для HTTP-настроек                                 |
| 5  | `server {}`            | http                   | Виртуальный хост (сайт)                                         |
| 6  | `listen`               | server                 | Порт/IP: `listen 80;`, `listen 443 ssl;`                        |
| 7  | `server_name`          | server                 | Домен сайта: `server_name example.com;`                         |
| 8  | `location {}`          | server, location       | Обработка путей: `location /api {}`                             |
| 9  | `root`                 | http, server, location | Путь к файлам: `root /var/www/html;`                            |
| 10 | `index`                | http, server, location | Главный файл: `index index.html;`                               |
| 11 | `proxy_pass`           | location, if           | Проксирование: `proxy_pass http://localhost:5000;`              |
| 12 | `proxy_set_header`     | location               | Заголовки: `proxy_set_header Host $host;`                       |
| 13 | `error_page`           | http, server, location | Своя страница ошибок: `error_page 404 /404.html;`               |
| 14 | `access_log`           | http, server, location | Путь к access-логу                                              |
| 15 | `error_log`            | main, http, server     | Путь к error-логу                                               |
| 16 | `include`              | любой                  | Подключение других конфигов                                     |
| 17 | `gzip`                 | http, server, location | Сжатие: `gzip on;`                                              |
| 18 | `gzip_types`           | http, server, location | MIME-типы для сжатия: `gzip_types text/html;`                   |
| 19 | `client_max_body_size` | http, server, location | Макс. размер запроса: `client_max_body_size 10M;`               |
| 20 | `rewrite`              | server, location, if   | Перезапись URL: `rewrite ^/old /new permanent;`                 |
| 21 | `return`               | server, location, if   | Возврат ответа: `return 301 https://$host$request_uri;`         |
| 22 | `try_files`            | location               | Проверка файлов: `try_files $uri $uri/ /index.html;`            |
| 23 | `expires`              | http, server, location | Кеширование: `expires 7d;`                                      |
| 24 | `add_header`           | http, server, location | Добавление заголовков: `add_header X-Frame-Options SAMEORIGIN;` |
| 25 | `ssl_certificate`      | http, server           | Путь к cert-файлу                                               |
| 26 | `ssl_certificate_key`  | http, server           | Путь к приватному ключу                                         |
| 27 | `ssl_protocols`        | http, server           | TLS-версии: `ssl_protocols TLSv1.2 TLSv1.3;`                    |
| 28 | `ssl_ciphers`          | http, server           | Шифры: `ssl_ciphers HIGH:!aNULL:!MD5;`                          |
| 29 | `log_format`           | http                   | Свой формат логов                                               |
| 30 | `limit_conn`           | http, server, location | Ограничение соединений: `limit_conn addr 1;`                    |
| 31 | `limit_req`            | http, server, location | Ограничение запросов                                            |
| 32 | `proxy_redirect`       | http, server, location | Управление Location-заголовками                                 |
| 33 | `proxy_cache`          | location               | Включение кэша                                                  |
| 34 | `proxy_cache_path`     | http                   | Настройка хранения кэша                                         |
| 35 | `resolver`             | http, server           | Указание DNS: `resolver 8.8.8.8;`                               |
| 36 | `keepalive_timeout`    | http, server, location | Таймаут соединения                                              |
| 37 | `default_type`         | http, server, location | MIME по умолчанию                                               |
| 38 | `client_body_timeout`  | http, server, location | Таймаут тела запроса                                            |
| 39 | `sendfile`             | http, server, location | Быстрая отдача файлов: `sendfile on;`                           |
| 40 | `tcp_nopush`           | http, server, location | Передача больших файлов                                         |
| 41 | `tcp_nodelay`          | http, server, location | Без задержек на маленькие пакеты                                |
| 42 | `alias`                | location               | Заменяет путь: `alias /srv/files/;`                             |
| 43 | `open_file_cache`      | http, server           | Кэширование мета-инфо о файлах                                  |
| 44 | `auth_basic`           | http, server, location | Включение HTTP Basic auth                                       |
| 45 | `auth_basic_user_file` | http, server, location | Указание .htpasswd                                              |
| 46 | `rewrite_log`          | http, server, location | Лог rewrite-операций                                            |
| 47 | `map`                  | http                   | Условные переменные                                             |
| 48 | `geo`                  | http                   | Переменные по IP-адресу                                         |
| 49 | `stub_status`          | location               | Мониторинг статуса NGINX                                        |
| 50 | `daemon`               | main                   | Запуск в фоне: `daemon off;` для Docker                         |



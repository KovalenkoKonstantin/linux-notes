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
| 2️⃣1️⃣ | `access_log` | `http`, `server`, `location` | Путь и формат лога доступа. <br>💡 `access_log /var/log/nginx/access.log;`                     |
| 2️⃣2️⃣ | `error_log`  | `main`, `http`, `server`     | Путь и уровень логов ошибок. <br>💡 `error_log /var/log/nginx/error.log warn;`                 |
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

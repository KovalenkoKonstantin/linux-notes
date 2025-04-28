## 🚀 Что делать для продакшена:

Чтобы сайт работал стабильно, безопасно и под нагрузкой, нужно использовать что-то вроде:

- **Gunicorn** — популярный WSGI сервер для Python
- **uWSGI** — тоже WSGI, но чуть сложнее в настройке
- **Nginx** — в связке с Gunicorn как **реверс-прокси**

---

🚀 Настроим автоматический запуск Flask-приложения через **Gunicorn + systemd**. Это будет стабильнее, безопаснее и не придётся вручную каждый раз запускать `python3 app.py`.

---

## ✅ Шаги для перехода на автоматический запуск

---

### 📦 1. Установка Gunicorn

Активируй своё виртуальное окружение, если ещё не:

```bash
source /var/www/local.work/venv/bin/activate
```

Установи Gunicorn:

```bash
pip install gunicorn
```

Проверь, что всё ок:

```bash
gunicorn --version
```

---

### ⚙️ 2. Тестовый запуск вручную

В папке `/var/www/local.work` запусти:

```bash
cd /var/www/local.work
gunicorn -w 4 -b 127.0.0.1:8001 app:app
```

> `app:app` означает:
> - первый `app` — имя файла `app.py`
> - второй `app` — это объект `Flask`, созданный внутри `app.py`

Будет что-то типа:

> (venv) rootubn@rootubn-VirtualBox:/var/www/local.work$ gunicorn -w 4 -b 127.0.0.1:8001 app:app
[2025-04-18 10:21:51 +0300] [45728] [INFO] Starting gunicorn 23.0.0
[2025-04-18 10:21:51 +0300] [45728] [INFO] Listening at: http://127.0.0.1:8001 (45728)
[2025-04-18 10:21:51 +0300] [45728] [INFO] Using worker: sync
[2025-04-18 10:21:51 +0300] [45729] [INFO] Booting worker with pid: 45729
[2025-04-18 10:21:51 +0300] [45730] [INFO] Booting worker with pid: 45730
[2025-04-18 10:21:51 +0300] [45731] [INFO] Booting worker with pid: 45731
[2025-04-18 10:21:51 +0300] [45732] [INFO] Booting worker with pid: 45732

Если всё работает — идём дальше.

Чтобы завершить тестовый запуск Gunicorn, просто нажми Ctrl + C в терминале — это остановит текущий процесс сервера.

Если хочешь проверить, что Gunicorn точно завершился и порт освободился:

```bash
sudo lsof -i :8001
```
`lsof`	**List Open Files** — утилита для показа файлов, открытых процессами
`-i :8001`	Показывает процессы, которые используют **сетевой порт 8001**

В Linux **порты — это тоже "файлы"**, и `lsof` может показать, кто их держит открытыми. Если кто-то слушает порт `8001`, эта команда покажет:

```bash
COMMAND   PID   USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
gunicorn  1234  root   3u  IPv4  123456      0t0  TCP 127.0.0.1:8001 (LISTEN)
```

Если команда ничего не выдает — всё чисто, сервер остановлен.

---

### 🛠️ 3. Изменим systemd-сервис (для запуска на 8001)

Создай новый файл сервиса:

```bash
sudo nano /etc/systemd/system/local.work.service
```

Вставь туда:

```ini
[Unit]
# Описание сервиса, которое будет отображаться в systemctl
Description=Gunicorn instance to serve local.work
# Это означает, что сервис будет запущен только после того, как сеть будет доступна.
After=network.target

[Service]
# Запуск сервиса от имени пользователя и группы www-data, чтобы избежать использования привилегий суперпользователя (root).
User=www-data
Group=www-data
# Указываем рабочую директорию для сервиса, чтобы gunicorn запускался из правильной папки.
WorkingDirectory=/var/www/local.work
# Указываем путь к виртуальному окружению, чтобы Python использовал его при запуске.
Environment="PATH=/var/www/local.work/venv/bin"
# Указываем команду для запуска gunicorn. Важно, чтобы путь к gunicorn указывал на виртуальное окружение (venv), чтобы использовать правильные зависимости.
ExecStart=/var/www/venv/bin/gunicorn -w 4 -b 127.0.0.1:8001 app:app

# Включает автоматический перезапуск сервиса в случае его падения.
Restart=always
# Задержка в 3 секунды перед перезапуском.
RestartSec=3

[Install]
# Это позволяет запускать сервис в многопользовательском режиме (обычно в обычной работе системы).
WantedBy=multi-user.target
```

**🔑 Моменты, которые нужно учитывать:**
* **Пользователь**: Запускать Gunicorn от имени пользователя `www-data`, потому что это более безопасно, чем запускать его от имени `root`.

* **Права на папки**: Убедись, что у пользователя `www-data` есть доступ к файлам проекта, а также к виртуальной среде Python (если ты хочешь её использовать).

**⚠️ Проверка прав доступа**
Перед тем, как использовать этого пользователя (`www-data`), нужно убедиться, что он имеет доступ к необходимым файлам и папкам:

Проверь права на проект (папки и файлы):

```bash
ls -l /var/www/local.work/ | grep app.py
```
Пример вывода:

```bash
-rwxrwxr-x 1 www-data www-data   1053 Apr 17 09:42 app.py
```

---

### 🔄 4. Перезагрузи systemd и запусти сервис

```bash
sudo systemctl daemon-reexec  # или daemon-reload (оба работают)
sudo systemctl start local.work
```

Проверь статус:

```bash
sudo systemctl status local.work
```

Будет что-то типа:

> (venv) rootubn@rootubn-VirtualBox:/var/www$ sudo systemctl daemon-reload
(venv) rootubn@rootubn-VirtualBox:/var/www$ sudo systemctl restart local.work
(venv) rootubn@rootubn-VirtualBox:/var/www$ sudo systemctl status local.work
● local.work.service - Gunicorn instance to serve local.work
     Loaded: loaded (/etc/systemd/system/local.work.service; disabled; preset: enabled)
     Active: active (running) since Fri 2025-04-18 11:04:45 MSK; 6s ago
   Main PID: 50013 (gunicorn)
      Tasks: 5 (limit: 11844)
     Memory: 81.3M (peak: 81.9M)
        CPU: 425ms
     CGroup: /system.slice/local.work.service
             ├─50013 /var/www/venv/bin/python3 /var/www/venv/bin/gunicorn -w 4 -b 127.0.0.1:8001 app:app
             ├─50015 /var/www/venv/bin/python3 /var/www/venv/bin/gunicorn -w 4 -b 127.0.0.1:8001 app:app
             ├─50016 /var/www/venv/bin/python3 /var/www/venv/bin/gunicorn -w 4 -b 127.0.0.1:8001 app:app
             ├─50018 /var/www/venv/bin/python3 /var/www/venv/bin/gunicorn -w 4 -b 127.0.0.1:8001 app:app
             └─50021 /var/www/venv/bin/python3 /var/www/venv/bin/gunicorn -w 4 -b 127.0.0.1:8001 app:app
Apr 18 11:04:45 rootubn-VirtualBox systemd[1]: Started local.work.service - Gunicorn instance to serve local.work.
Apr 18 11:04:45 rootubn-VirtualBox gunicorn[50013]: [2025-04-18 11:04:45 +0300] [50013] [INFO] Starting gunicorn 23.0.0
Apr 18 11:04:45 rootubn-VirtualBox gunicorn[50013]: [2025-04-18 11:04:45 +0300] [50013] [INFO] Listening at: http://127.0.0.1:8001 (50013)
Apr 18 11:04:45 rootubn-VirtualBox gunicorn[50013]: [2025-04-18 11:04:45 +0300] [50013] [INFO] Using worker: sync
Apr 18 11:04:45 rootubn-VirtualBox gunicorn[50015]: [2025-04-18 11:04:45 +0300] [50015] [INFO] Booting worker with pid: 50015
Apr 18 11:04:45 rootubn-VirtualBox gunicorn[50016]: [2025-04-18 11:04:45 +0300] [50016] [INFO] Booting worker with pid: 50016
Apr 18 11:04:46 rootubn-VirtualBox gunicorn[50018]: [2025-04-18 11:04:46 +0300] [50018] [INFO] Booting worker with pid: 50018
Apr 18 11:04:46 rootubn-VirtualBox gunicorn[50021]: [2025-04-18 11:04:46 +0300] [50021] [INFO] Booting worker with pid: 50021

Если всё ок:
✅ Включить автозапуск при загрузке системы:
```bash
sudo systemctl enable local.work
```
✅ Проверить, что сервер реально отдаёт ответ:

```bash
curl http://127.0.0.1:8001
```

Теперь Flask будет запускаться **автоматически при загрузке системы**.

---

### 🌐 5. Убедись, что Nginx проксирует на `127.0.0.1:8001`

Пример конфига:

```nginx
server {
    listen 80;
    server_name local.work;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /var/www/local.work/static/;
    }

    location /images/ {
        alias /var/www/local.work/images/;
    }
}
```

Проверь и перезапусти Nginx:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

**Проверь доступность с использованием** `curl`: После того как ты перезагрузил Nginx, проверь, доступен ли сайт:

```bash
curl http://10.121.1.24/
```
Если всё настроено правильно, ты должен получить ответ от твоего Flask-приложения.

**Проверь правильность работы Gunicorn**: Убедись, что Gunicorn работает на порту `8001`, как мы уже обсуждали ранее. Для этого можно использовать команду:

```bash
sudo lsof -i :8001
```
Если Gunicorn не работает, запусти его снова:

```bash
gunicorn --bind 127.0.0.1:8001 app:app
```

---

### 1. **Перезапуск Gunicorn**
   - Если вы не видите изменений, это может быть связано с тем, что Gunicorn не перезагрузился после внесения изменений в код. Для того чтобы обновления вступили в силу, нужно либо перезапустить Gunicorn, либо использовать параметр `--reload`, который автоматически перезагружает сервер при изменении исходных файлов.

   Если вы запускаете его вручную, завершите все процессы и запустите снова:
   ```bash
   sudo pkill gunicorn
   local.work -w 4 app:app
   ```

   **Если вы хотите использовать автоматическую перезагрузку (при разработке):**
   Запустите Gunicorn с флагом `--reload`:
   Измените строку `ExecStart` в вашем **Systemd** файле на следующую:
   ```bash
   sudo nano /etc/systemd/system/local.work.service
   ```
   ```bash
   ExecStart=/var/www/venv/bin/gunicorn --reload -w 4 -b 127.0.0.1:8001 app:app
   ```
**Перезагрузка и активация сервиса:**

```bash
cd /var/www/local.work
sudo systemctl daemon-reload
sudo systemctl restart local.work
sudo systemctl enable local.work
```
**Проверка статуса сервиса:**
```bash
sudo systemctl list-units --type=service | grep Gunicorn
sudo systemctl status local.work
```

---
## 🎉 Готово!

Теперь Flask автоматически поднимается через Gunicorn как системный сервис.
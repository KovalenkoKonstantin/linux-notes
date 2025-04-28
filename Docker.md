
## 🧱 1. **Удалим старые версии (если вдруг что-то было)**
```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

---

## 📦 2. **Установим Docker (через официальный репозиторий)**

```bash
sudo apt-get update

sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

Добавим Docker GPG-ключ:

```bash
sudo mkdir -m 0755 -p /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

Добавим Docker репозиторий:

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

---

## 📥 3. **Установка Docker Engine**

```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
**Добавь прокси для Docker (с логином и паролем)**

Создай (или отредактируй) файл:

```bash
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo nano /etc/systemd/system/docker.service.d/http-proxy.conf
```
Добавь в файл:

```ini
[Service]
Environment="HTTP_PROXY=http://USERNAME:PASSWORD@proxy-server:PORT/"
Environment="HTTPS_PROXY=http://USERNAME:PASSWORD@proxy-server:PORT/"
Environment="NO_PROXY=localhost,127.0.0.1"
```

Перезапусти Docker и проверь, что всё работает:

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl restart docker
```

```bash
sudo docker run hello-world
```
В ответ должно прийти

```bash
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

---

## ✅ 4. **Добавим себя в группу `docker`, чтобы не писать `sudo`**

```bash
sudo usermod -aG docker $USER
```

Затем **перезайди в сессию** (или просто выполни `newgrp docker`).

**Проверьте группу пользователя**: После того как вы добавили пользователя в группу docker, можно проверить, что ваш пользователь входит в эту группу, выполнив команду:

```bash
groups $USER
```
Убедитесь, что среди групп есть `docker`.

---

## 🧩 5. **Проверка Docker Compose**

Теперь `docker compose` (с пробелом!) уже встроен. Проверь:

```bash
docker compose version
```

🔥 Если видишь версию — отлично, и Docker, и Compose уже установлены и работают!

---

Теперь можно перейти к следующему шагу — **создание `Dockerfile` и `docker-compose.yml`** для упаковки твоего проекта.  
Раз уж у тебя Flask + NGINX, предлагаю пойти по **двухконтейнерной схеме**:  
1. Контейнер с Flask-приложением  
2. Контейнер с NGINX, проксирующим на Flask  

---

### 1. Создаём `Dockerfile` для Flask-приложения в директории `/www/local.work`

```bash
cd /var/www/local.work
```

```bash
nano Dockerfile
```

```Dockerfile

# Dockerfile — это просто документация для других разработчиков (и Docker'а)

# Используем официальный базовый образ Python 3.10 на базе slim (облегчённый Debian)
FROM python:3.10-slim

# Получаем значения из ARG
ARG HTTP_PROXY
ARG HTTPS_PROXY

# Прокидываем в ENV
ENV http_proxy=$HTTP_PROXY
ENV https_proxy=$HTTPS_PROXY

# Прокси для apt (создаётся файл конфигурации на лету)
RUN echo "Acquire::http::Proxy \"${HTTP_PROXY}\";" > /etc/apt/apt.conf.d/01proxy

# Установка системных зависимостей для WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*
# rm -rf /var/lib/apt/lists/*	Удаляет кэш apt после установки, снижает размер образа

# Устанавливаем рабочую директорию внутри контейнера (всё будет происходить в /app)
WORKDIR /app

# Копируем все файлы из текущей директории на хосте (где находится Dockerfile) в директорию /app в контейнере
COPY ./ /app

# Обновляем pip до последней версии и устанавливаем зависимости из файла requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Открываем порт 5000 внутри контейнера для взаимодействия с Flask-приложением (по умолчанию Flask работает на этом порту)
# не участвует в пробросе портов
# EXPOSE не меняет поведение контейнера — это просто "подсказка" Docker'у и другим людям.
EXPOSE 6000

# Задаём команду, которая будет выполнена при запуске контейнера:
# Запускаем файл app.py с Python (ожидается, что в app.py есть запуск Flask-сервера)
CMD ["python", "app.py"]


```
в той же папке (`/var/www/local.work`) генерируем requirements.txt

`requirements.txt` можно сгенерировать командой:  
```bash
pip freeze > requirements.txt
```

Но, лучше использовать реалиные зависимости проекта

Вот **чистый `requirements.txt`**, составленный **по реальному использованию библиотек**:

```txt
Flask==2.3.3
requests==2.31.0
num2words==0.5.12
Jinja2==3.1.2
WeasyPrint==61.2
PyPDF2==3.0.1
```

### Комментарии по зависимостям:
| Библиотека      | Зачем нужна                              |
|------------------|-------------------------------------------|
| `Flask`          | Основной фреймворк                        |
| `requests`       | Внешние HTTP-запросы                      |
| `num2words`      | Преобразование чисел в слова              |
| `Jinja2`         | Используется Flask'ом, можно явно указать |
| `WeasyPrint`     | Генерация PDF                             |
| `PyPDF2`         | Слияние PDF                               |

---

### 💡 Советы:

- **`sqlite3`**, `os`, `datetime`, `math`, `re`, `json` — это встроенные библиотеки Python, их не надо указывать.
- **`Brlapi`**, `dbus-python`, `pycups`, `systemd-python`, `cloud-init` и т.п. — это нативные системные библиотеки, не ставятся через `pip` и не нужны тебе для Flask-приложения.
- Можно добавить `gunicorn`, если хочешь production-сервер:
  ```txt
  gunicorn==21.2.0
  ```
---

### 2. Создаём `docker-compose.yml`

```bash
nano docker-compose.yml
```

---

### 3. Пишем `docker-compose.yml`

```yaml
# version: '3.8'  С Docker Compose v2 (а у тебя именно он) директива version: устарела и не нужна вовсе.

services:
  flask-app:
    build:                                                  # build: указывает на директорию с Dockerfile относительно docker-compose.yml
      context: .
      args:
        HTTP_PROXY: ${HTTP_PROXY}
        HTTPS_PROXY: ${HTTPS_PROXY}
    container_name: flask-app                               # Монтируется локальная директория local.work в контейнер
    ports:
      - "5000:5000"                                         # правило проброса портов Первый 6000 — внешний порт хоста, Второй 5000 — внутренний порт контейнера
      - "8000:8000"
    volumes:                                                # volume — проброс папки хоста в контейнер
      - .:/app                                              # Монтируем текущую директорию в контейнер . — относительный путь где код. /app — путь внутри контейнера, куда этот код монтируется.
      - ./settings/local.work:/etc/nginx/sites-enabled/     # Монтируется конфиг Nginx
      - ./data:/app/data                                    # Пробрасываем папку с данными в /app/data внутри контейнера
    networks:
      - mynetwork                                           # сеть, в которой работает Flask
    environment:                                            # Настройки прокси
      - http_proxy=${HTTP_PROXY}
      - https_proxy=${HTTPS_PROXY}
      - FLASK_ENV=development
    restart: unless-stopped                                 # ✅ unless-stopped — перезапускается всегда, кроме случая, когда ты сам вручную его остановил.

  nginx:
    image: nginx:latest                                     # Используется стандартный образ nginx:latest
    container_name: nginx-container
    ports:
      - "80:80"                                             # 80 на хосте → 80 в контейнере (завязано на 80 порт в настройках nginx -> server listen 80)
    volumes:                                                # volume — проброс папки хоста в контейнер
      - ./settings/nginx.conf:/etc/nginx/nginx.conf         # Основной конфиг nginx
      - ./settings/local.work:/etc/nginx/sites-enabled/     # Конфиг сервера
      - ./static:/app/static                                # Отдача статики
      - ./templates:/app/templates                          # Корень сайта
      - ./local.work:/app                                   # Docker будет запускать app.py из /app/app.py, но код будет синхронизирован с ./local.work
      - ./shared:/app/shared                                # Общая папка (если есть)
    depends_on:
      - flask-app                                           # Убедимся, что Flask запущен до Nginx
    networks:
      - mynetwork                                           # сеть, в которой работает nginx

networks:
  mynetwork:
    driver: bridge                                          # bridge — стандартная дефолтная сеть Docker

```

# Шаги для создания и подключения сети:
1. **Создание сети Docker**: Создайте новую сеть `mynetwork`:

```bash
docker network create mynetwork
```

2. **Отключить контейнеры от всех сетей:**

Для каждого контейнера выполните команду, чтобы убедиться, что они не подключены к другим сетям:

```bash
docker network disconnect bridge flask-app
docker network disconnect bridge nginx-container
```

2. **Перезапуск контейнеров с подключением к сети**: Теперь нужно перезапустить контейнеры с использованием этой сети. Отключите контейнеры от текущих сетей (если они подключены) и подключите их к `mynetwork`.

  Для каждого контейнера выполните:

  ```bash
  docker run --network mynetwork -d --name flask-app localwork-flask-app
  docker run --network mynetwork -d --name nginx-container nginx
  ```
3. **После этого снова проверьте статус контейнеров с помощью**:

  ```bash
  docker ps
  ```
**Проверка:**
Теперь контейнеры `flask-app` и `nginx-container` успешно запущены и подключены к сети mynetwork. Чтобы проверить, могут ли они взаимодействовать друг с другом, попробуйте выполнить следующие команды:

В контейнере Flask попытайтесь обратиться к Nginx с помощью `curl`:

```bash
docker exec -it flask-app curl nginx-container:80
```
В контейнере Nginx попробуйте обратиться к Flask:

```bash
docker exec -it nginx-container curl flask-app:5000
```

**Получите имена образов контейнеров:**

Используйте команду `docker images`, чтобы увидеть список доступных образов на вашей машине.

```bash
docker images
```

---

### 🔹 Шаг 1: Создай `.env` файл

Создай файл `.env` в директории, где у тебя находится `docker-compose.yml`, то есть в `/var/www/local.work/`.

```bash
nano .env
```

---

### 🔹 Шаг 2: Пропиши переменные окружения

В `.env` укажи свой логин, пароль и прокси-сервер. Например:

```env
HTTP_PROXY=http://your-login:your-password@your.proxy.server:port
HTTPS_PROXY=http://your-login:your-password@your.proxy.server:port
```

⚠️ **Если в логине или пароле есть спецсимволы (например, `@`, `:`, `/` и т.п.), их надо экранировать или использовать URL-кодировку**:
- `@` → `%40`
- `:` → `%3A`
- `/` → `%2F`
- `,` → `%2C`

проверить корректность заполнения

Запустите контейнер без выполнения команд:

```bash
docker run --env-file /var/www/local.work/.env -it python:3.10-slim /bin/bash
```
После входа в контейнер, проверьте:

```bash
echo $HTTP_PROXY
echo $HTTPS_PROXY
```

---

### 🔹 Следующий шаг

После этого ты можешь запускать контейнеры:

```bash
docker compose up --build
```
Это одна команда, которая делает **две вещи**:

1. `--build` — сначала **собирает образ** (по `Dockerfile`).
2. Затем **запускает контейнеры** (по `docker-compose.yml`).

🙌


Чтобы остановить контейнеры, можно использовать команду:

```bash
docker compose down
```

Чтобы остановить контейнеры, используйте команду:

```bash
docker stop flask-app
```

Чтобы удалить контейнеры:
```bash
docker rm flask-app
```
Чтобы отобразить работающие контейнеры

```bash
docker ps
```
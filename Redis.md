## ⚡ Подключение Redis — зачем и как

### ❓ Зачем Redis:

| Возможность       | Где применимо в твоем проекте                  |
|-------------------|------------------------------------------------|
| 🔁 Кэш             | Кэшировать employee.json и registry.json       |
| 📋 Очереди         | Фоновая обработка (approve, reject, обновление) |
| 🔐 Сессии/Токены   | Хранить токены или временные коды доступа     |
| ✅ Проверка сотрудников | Кэш результатов в `check_employee`           |

---

### 🔌 Установка и подключение

**Установка (на сервере/локально):**
```bash
sudo apt install redis
pip install redis
```

**Базовое подключение:**
```python
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
```
**Проверка, запущен ли Redis**

```bash
sudo systemctl status redis
```

---

### 💡 Примеры применения

**Превращаем fetch_data.py в фоновую задачу**

**В файле `/var/www/local.work/config.py`**

прописываем:
```bash

import os

class Config:
    """Основные настройки для Flask приложения"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fucking_incredibly_secret_key')  # Лучше использовать переменные окружения
    STATIC_FOLDER = '/var/www/local.work/static'  # Путь к статическим файлам
    TEMPLATE_FOLDER = '/var/www/local.work/templates'  # Путь к папке с шаблонами

    # Redis как брокер и backend
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
```

**В файле `/var/www/local.work/tasks/celery_tasks.py`**

прописываем:
```bash
from celery import Celery
from config import Config
import os, json, requests

# Настроим Celery с использованием Redis в качестве брокера
celery_app = Celery('tasks', broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

celery_app.conf.timezone = 'Europe/Moscow'

@celery_app.task
def fetch_and_store_employee_data():
    #Фоновая задача — получить данные с удалённого API и сохранить в файл
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
```

**Устанавливаем зависимости**

```bash
pip install celery redis
```

**📦 Запуск Celery Worker**

В корне проекта (где `tasks/celery_tasks.py`), запусти:

```bash
cd /var/www/local.work/
celery -A tasks.celery_tasks.celery_app worker --loglevel=info
```

**🧠 Что это значит**
`-A tasks.celery_tasks.celery_app` — указывает на путь к твоему Celery-приложению (как к Python-модулю),

`worker` — запуск воркера (он будет ждать задач из Redis),

`--loglevel=info` — просто удобный уровень логов (покажет, что происходит).

Когда ты запускаешь воркер с командой:

```bash
celery -A tasks.celery_tasks.celery_app worker --loglevel=info
```
Celery подключается к Redis как к брокеру сообщений (согласно настройкам в `Config.CELERY_BROKER_URL`). В этом случае воркер будет слушать очередь Redis и забирать задачи, как только они поступят. После выполнения задачи результат сохраняется в Redis, если настроен `CELERY_RESULT_BACKEND`.


**🧪 Как проверить?**
Открой Python в виртуалке:

```bash
source /var/www/venv/bin/activate
```
```bash
cd local.work/
```

```bash
python
```

А внутри:

```python
from tasks.celery_tasks import fetch_and_store_employee_data
fetch_and_store_employee_data.delay()
```

Теперь задача была успешно поставлена в очередь Celery, и ты получил объект `AsyncResult`, который указывает на статус выполнения задачи. Этот объект используется для отслеживания состояния задачи и получения результата.

Если ты хочешь проверить статус выполнения задачи, можешь сделать следующее:

1. Чтобы узнать, завершена ли задача, используй метод `.status`:

```python
print(fetch_and_store_employee_data.delay().status)
```

2. Если хочешь получить результат задачи (если она уже завершена), используй метод `.get()`:

```python
result = fetch_and_store_employee_data.delay().get()
print(result)
```

Обрати внимание, что `.get()` может блокировать выполнение, пока задача не завершится, если результат ещё не получен.

Таким образом, ты можешь контролировать процесс выполнения задач через Celery и Redis.

















#### ✅ Кэш `employee.json`

```python
def get_employees():
    cache_key = "employees"

    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)

    with open("data/employee.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        r.set(cache_key, json.dumps(data), ex=3600)  # кэш на 1 час
        return data
```

#### 📥 Очередь на обновление данных (pub/sub)

Пушим в Redis:
```python
r.publish("data_updates", "registry_updated")
```

Слушатель (отдельный процесс):
```python
pubsub = r.pubsub()
pubsub.subscribe("data_updates")

for message in pubsub.listen():
    if message['type'] == 'message':
        print("Обновить данные:", message['data'])
```

---

## 📁 Структурно можно добавить:

```
/config
    __init__.py
    default.py
/services
    employee_service.py
    registry_service.py
/cache
    redis_client.py     # подключение и утилиты для Redis
/cli
    update_registry.py  # CLI-команды типа обновить json
/tests
    test_registry.py
```

---

## ✨ Бонус: flask-caching (если хочешь быстро кэшить)

```bash
pip install flask-caching
```

```python
from flask_caching import Cache

cache = Cache(app, config={"CACHE_TYPE": "RedisCache", "CACHE_REDIS_URL": app.config['REDIS_URL']})

@cache.cached(timeout=3600)
def get_registry():
    ...
```

---

Хочешь — помогу с конкретным примером подключения Redis к `fetch_data.py` или API-кэшированием.
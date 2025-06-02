
### 📦 1. Установка SQLite

На Ubuntu/Debian:

```bash
sudo apt update
sudo apt install sqlite3
```

---

### 🗃 2. Создание базы данных

Создадим файл базы:

```bash
sqlite3 /var/www/local.work/data/local.db
```
эта команда войдёт в интерактивную консоль `sqlite3`

Внутри консоли SQLite:

```sql
-- Таблица для registry
CREATE TABLE registry (
    id INTEGER PRIMARY KEY,
    data TEXT
);

-- Таблица для employee
CREATE TABLE employee (
    id INTEGER PRIMARY KEY,
    data TEXT
);

.quit
```

---

### 🧠 3. Скрипт для трансляции JSON → SQLite


```python
import json
import sqlite3
from pathlib import Path

DB_PATH = Path("/var/www/local.work/data/local.db")
REGISTRY_JSON = Path("/var/www/local.work/data/registry.json")
EMPLOYEE_JSON = Path("/var/www/local.work/data/employee.json")

def decode_unicode(json_obj):
    if isinstance(json_obj, dict):
        return {k: decode_unicode(v) for k, v in json_obj.items()}
    elif isinstance(json_obj, list):
        return [decode_unicode(item) for item in json_obj]
    elif isinstance(json_obj, str):
        try:
            return json_obj.encode('latin1').decode('utf-8')  # Фиксировка кракозябр
        except UnicodeEncodeError:
            return json_obj
    return json_obj

def load_and_decode_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [decode_unicode(item) for item in data]

def sync_json_to_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("🧹 Очищаем таблицы...")
    cur.execute("DELETE FROM registry")
    cur.execute("DELETE FROM employee")

    print("📥 Загружаем и декодируем registry.json...")
    registry_data = load_and_decode_json(REGISTRY_JSON)
    for item in registry_data:
        cur.execute("INSERT INTO registry (data) VALUES (?)", (json.dumps(item, ensure_ascii=False),))

    print("📥 Загружаем и декодируем employee.json...")
    employee_data = load_and_decode_json(EMPLOYEE_JSON)
    for item in employee_data:
        cur.execute("INSERT INTO employee (data) VALUES (?)", (json.dumps(item, ensure_ascii=False),))

    conn.commit()
    conn.close()
    print("✅ Синхронизация завершена.")

if __name__ == "__main__":
    sync_json_to_db()
```

---

### 🛠 Пример запуска:

```bash
python3 /var/www/local.work/scripts/sync_json_to_db.py
```

---

### 🔁 4. Настройка периодического обновления (опционально)

Через планировщик заданий `cron`:

Чтобы настроить автоматический запуск скрипта раз в сутки, откройте файл crontab для редактирования:
```bash
crontab -e
```
Если вы используете первый раз, вам предложат выбрать редактор (например, nano).

В файле crontab добавьте следующую строку для выполнения скрипта каждый день в определенное время, например, в 3:00 утра:

```bash
0 3 * * * /var/www/venv/bin/python /var/www/local.work/scripts/sync_json_to_db.py
```

Здесь:

* `0 3 * * *` — это время и дата. Это означает, что задание будет выполняться в 3:00 утра каждый день.

* `/var/www/venv/bin/python` — путь к интерпретатору Python 3. Убедитесь, что это правильный путь для вашей системы. Вы можете узнать его с помощью команды `which python3`.

* `/var/www/local.work/scripts/sync_json_to_db.py` — путь к вашему скрипту.

Чтобы проверить, что задача добавлена, вы можете использовать команду:

```bash
crontab -l
```

Чтобы настроить выполнение вашего скрипта каждые 5 минут с помощью cron, вам нужно изменить запись в crontab. Вот как это сделать:

```bash
*/5 * * * * /var/www/venv/bin/python /var/www/local.work/scripts/sync_json_to_db.py
```

`*/5` — это означает "каждые 5 минут".

**бросить счётчик `id` в SQLite**

```bash
DELETE FROM sqlite_sequence WHERE name='users';
```
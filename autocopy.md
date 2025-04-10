# Автоматическое копирование актуального лога в папку. Это удобно, безопасно и не зависит от ротации.

---

## 📌 Цель:
Копировать актуальный `/var/log/nginx/access.log` → в `/var/www/logs/access.log`
b
`/var/log/nginx/error.log` → в `/var/www/logs/access.log`
, **каждую минуту**.

---

## 🔧 Шаг 1: Создаём скрипт

1. Открой терминал и создай файл:

```bash
sudo nano /usr/local/bin/copy_nginx_logs.sh
```

2. Вставь в файл вот это:

```bash
cp /var/log/nginx/access.log /var/www/logs/access.log
chown www-data:www-data /var/www/logs/access.log
chmod 644 /var/www/logs/access.log
cp /var/log/nginx/error.log /var/www/logs/error.log
chown www-data:www-data /var/www/logs/error.log
chmod 644 /var/www/logs/error.log
```

> Это просто копирует лог, выставляет нужные права, чтобы Nginx и браузер могли читать.

3. Сохрани и выйди:
- `Ctrl+O` → Enter
- `Ctrl+X`

4. Сделай скрипт исполняемым:

```bash
sudo chmod +x /usr/local/bin/copy_nginx_logs.sh
```
---
## ⏰ Шаг 2: Добавляем в `cron`

Откроем `crontab` от `root`, чтобы был доступ ко всем файлам:

```bash
sudo crontab -e
```

Добавь в самый низ строку:
В `cron` минимальный интервал — 1 минута. Строка в crontab:
```bash
* * * * * /usr/local/bin/copy_nginx_logs.sh
```
означает: **каждую минуту в 0 секунд** выполняется скрипт.

---

## ✅ Шаг 3: Проверка

Подожди 1-2 минуты, потом выполни:

```bash
ls -l /var/www/logs/access.log
```

и

```bash
tail /var/www/logs/access.log
```

Ты должен увидеть свежие записи. Если лог пустой — возможно, сайт никто не посещал.

---

## 🧪 Проверка в реальном времени

Открой сайт со своего браузера или с другого устройства (зайди на http://10.121.1.164), потом снова проверь:

```bash
tail /var/www/settings/access.log
```

Ты увидишь, какой IP заходил и какие запросы отправлял.

## 🤔 А если хочешь каждые 30 секунд?
Классический `cron` **не умеет запускать задачи чаще, чем раз в минуту.** Но есть варианты обойти это:


### ✅ **Вариант 1: Два запуска через `cron` (немного костыль, но рабочий)**

Открываешь `sudo crontab -e` и добавляешь **два задания**:

```bash
* * * * * /usr/local/bin/copy_nginx_log.sh
* * * * * sleep 30 && /usr/local/bin/copy_nginx_log.sh
```

Первая — выполняется в начале каждой минуты, вторая — через 30 секунд после начала. Получается копирование **раз в 30 секунд**.

> `sleep 30` заставляет вторую задачу подождать полминуты перед выполнением.

---

### ✅ **Вариант 2: Запуск скрипта в фоновом цикле (надежнее, но требует systemd или screen)**

Если хочешь более гибко и точно, можно сделать бесконечный цикл с `sleep 30`:

1. Создай новый скрипт:

```bash
sudo nano /usr/local/bin/copy_nginx_loop.sh
```

2. Вставь в него:

```bash
#!/bin/bash
while true; do
    /usr/local/bin/copy_nginx_log.sh
    sleep 30
done
```

3. Сделай исполняемым:

```bash
sudo chmod +x /usr/local/bin/copy_nginx_loop.sh
```

4. Запусти в фоне через `screen` или `nohup`:

```bash
nohup /usr/local/bin/copy_nginx_loop.sh &
```

> `nohup` = не завершится при выходе из сессии.


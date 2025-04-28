Подключение к Ubuntu VM по SSH через VS Code — это 🔥 способ работать прямо на сервере, но в удобной графике, как будто ты у себя локально.

---

## ✅ Что понадобится:

- ✅ Установленный [Visual Studio Code](https://code.visualstudio.com/)
- ✅ Расширение **Remote - SSH** (бесплатное)
- ✅ IP-адрес и логин от Ubuntu VM
- ✅ Открытый порт SSH (обычно `22`) на VM
- ✅ Доступ по паролю или SSH-ключу

---

## 🛠️ Шаги

### 1. Установи расширение Remote - SSH

1. Открой VS Code.
2. Перейди в Extensions (Ctrl+Shift+X).
3. В поиске напиши: `Remote - SSH`.
4. Установи его (автор — Microsoft).

🔗 Или прямая ссылка:  
https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh

---

### 2. Подключение к Ubuntu по IP

1. Нажми F1 или Ctrl+Shift+P, чтобы открыть командную палитру.
2. Введи: `Remote-SSH: Connect to Host...`
3. Нажми **+ Add New SSH Host...**
4. Введи строку подключения (пример ниже):

```
ssh rootubn@10.121.1.164
ssh rootubn@10.121.1.24
```

👉 Здесь:
- `rootubn` — имя пользователя в Ubuntu.
- `10.121.1.164` — IP твоей Ubuntu VM (можно узнать командой `ip a` внутри VM).

5. Выбери, куда сохранить — лучше `C:\Users\Kovalenko.Kon\.ssh\config` (Windows).

---
### 3. Настроить SSH на виртуальной машине
Открой терминал внутри `Ubuntu VM`
1. Убедись, что установлен SSH-сервер:
```bash
sudo apt update
sudo apt install openssh-server
```
2. Установи пакет openssh-server
```bash
sudo apt update -y
sudo apt install -y openssh-server
```
3. Запусти SSH-сервер:
```bash
sudo systemctl start ssh
```
4. Проверь его статус:
```bash
sudo systemctl status ssh
```
Увидишь что-то типа:

```yaml
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/usr/lib/systemd/system/ssh.service; disabled; preset: enabled)
     Active: active (running) since Thu 2025-04-10 13:53:06 MSK; 12s ago
```
Если `active (running)` — 🎉 значит, SSH работает.

---
### 4. Подключись к хосту

1. Снова `F1` → `Remote-SSH: Connect to Host...`
2. Выбери только что добавленный хост.
3. Выбери операционную систему.
4. Введи пароль.
4. 💥 Всё! Откроется новое окно VS Code — **уже внутри Ubuntu VM!**

---

### 5. Работай как дома

Теперь ты можешь:
- Открывать папки (`/var/www/...`)
- Редактировать `app.py`, `index.html`, JS, CSS — **в реальном времени на сервере**
- Открывать терминал прямо в VS Code (Ctrl+`) — это будет терминал VM
- Запускать Flask, проверять nginx и так далее

---

## 🤖 Дополнительно: подключение по ключу SSH (опционально)

Если не хочешь вводить пароль каждый раз — настрой ключ:
1. В Windows создай ключ:  
```bash
ssh-keygen -t rsa
```

2. Скопируй ключ на Ubuntu VM:  
```bash
ssh-copy-id user@ip_vm
```

Теперь VS Code будет логиниться без пароля.

---

## 🧠 Полезные команды в терминале VS Code:

```bash
cd /var/www/html             # перейти в папку сайта
sudo systemctl status nginx  # статус nginx
python3 app.py               # запустить Flask
```
Visual Studio Code (VSCode) — вот как установить его на Ubuntu:

### 🔧 Установка VSCode на Ubuntu

Открой терминал и выполни следующие команды:

1. **Обнови индекс пакетов:**
```bash
sudo apt update
```

2. **Установи зависимости (если ещё не установлены):**
```bash
sudo apt install software-properties-common apt-transport-https wget
```

3. **Добавь репозиторий Microsoft и GPG ключ:**
```bash
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
```

4. **Установи VSCode:**
```bash
sudo apt update
sudo apt install code
```

После этого можно запускать редактор командой:
```bash
code
```

Хочешь, я сгенерю скрипт, который всё это делает автоматически?
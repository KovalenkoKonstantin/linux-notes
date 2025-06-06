Чтобы установить Chromium, скачанный из архива (https://download-chromium.appspot.com/dl/Linux_x64?type=snapshots), выполните следующие шаги.

### 1. **Распаковка архива**

После того как вы скачали архив с Chromium, вам нужно его распаковать. Откройте терминал и перейдите в каталог, куда вы скачали файл. Например, если файл скачан в папку `~/Downloads`, выполните:

```bash
cd ~/Downloads
```

Затем распакуйте архив:

```bash
sudo apt install -y unzip
unzip chrome-linux.zip
```

После этого у вас появится папка с названием, например, `chrome-linux`.

### 2. **Перемещение в удобное место**

Рекомендуется переместить распакованную папку в директорию `/opt`, которая предназначена для установленных приложений в Linux:

```bash
sudo mv chrome-linux /opt/chromium
```

### 3. **Создание ярлыка (desktop entry)**

Теперь создайте ярлык для Chromium, чтобы запускать его из меню приложений или через команду в терминале. Для этого создайте новый файл в папке `~/.local/share/applications/`:

```bash
nano ~/.local/share/applications/chromium.desktop
```

Вставьте в файл следующий текст:

```plaintext
[Desktop Entry]
Name=Chromium
Exec=/opt/chromium/chrome --no-sandbox %U
Icon=/opt/chromium/product_logo_48.png
Type=Application
Categories=Network;WebBrowser;
StartupWMClass=Chromium
```

Сохраните файл (`CTRL+O`, затем `ENTER`) и закройте редактор (`CTRL+X`).

### 4. **Предоставление прав на выполнение**

Для того чтобы запускать Chromium, нужно предоставить права на выполнение. Выполните команду:

```bash
sudo chmod +x /opt/chromium/chrome
```

### 5. **Запуск Chromium**

Теперь вы можете запустить Chromium с помощью команды:

```bash
/opt/chromium/chrome --no-sandbox
```

Или, если вы создали ярлык, просто найдите Chromium в меню приложений и запустите его оттуда.

### 6. **Использование Chromium без sandbox (опционально)**

Chromium может требовать флага `--no-sandbox`, чтобы работать без ошибок в некоторых системах. Этот флаг отключает механизм безопасности, который может не работать в определённых окружениях.

Если вы хотите запускать Chromium без флага `--no-sandbox`, можете просто удалить его из ярлыка или командной строки, но имейте в виду, что это может повлиять на безопасность.

### Дополнительные рекомендации:

- Если вы хотите, чтобы Chromium всегда запускался с графическим интерфейсом, используйте ярлык из меню.
- Вы можете добавить путь `/opt/chromium` в ваш системный `PATH`, чтобы запускать Chromium из терминала с любой директории.

Теперь у вас установлен Chromium, и вы можете им пользоваться на своей системе!
""" Этот скрипт можно использовать для настройки локальной переадресации доменов в целях тестирования, 
разработки или других нужд, когда требуется вручную сопоставить домен с конкретным IP-адресом. """

import os
import sys

# Настройки
HOSTS_PATH = {
    'nt': r'C:\Windows\System32\drivers\etc\hosts',  # Windows
    'posix': '/etc/hosts'                            # Linux / macOS
}

IP_ADDRESS = '10.121.1.24'
DOMAIN_NAME = 'local.work'

def get_hosts_path():
    if os.name == 'nt':
        return HOSTS_PATH['nt']
    else:
        return HOSTS_PATH['posix']

def add_host_entry():
    hosts_path = get_hosts_path()

    # Проверка наличия файла и прав доступа
    if not os.path.exists(hosts_path):
        print(f"Файл {hosts_path} не найден.")
        sys.exit(1)

    # Читаем текущие содержимое файла
    with open(hosts_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Проверяем, есть ли уже нужная запись
    entry = f"{IP_ADDRESS}\t{DOMAIN_NAME}\n"
    for line in lines:
        if DOMAIN_NAME in line:
            print(f"Запись для {DOMAIN_NAME} уже существует.")
            return

    # Добавляем новую запись
    try:
        with open(hosts_path, 'a', encoding='utf-8') as f:
            f.write(entry)
        print(f"Запись успешно добавлена: {entry.strip()}")
    except PermissionError:
        print("Ошибка доступа. Запустите скрипт с правами администратора.")
        sys.exit(1)

if __name__ == '__main__':
    add_host_entry()
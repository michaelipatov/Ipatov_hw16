import json
from pathlib import Path


def load_file(file_name):
    """Возвращает список словарей из json-файлов в папке data"""
    home = Path.home()
    path = Path(home, 'PycharmProjects', 'Ipatov_hw16', 'data', file_name)
    with open(path, encoding="utf-8") as file:
        json_list = json.load(file)
        return json_list

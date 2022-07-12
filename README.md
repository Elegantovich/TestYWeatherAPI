# TestYWeatherAPI

![Status](https://github.com/elegantovich/TestYWeatherAPI/actions/workflows/main.yml/badge.svg)
## Description
Проект для обработки данных с интерфейса сервиса "Яндекс Погода".

### Tech
Python 3.10, Selenium 4.3, Pandas 1.3, Django 3.2, RF


### How to start a project:
Тестирование производилось на браузере Google chrome. Для старта необходимо узнать версию браузера.
```
chrome://settings/help
```
Скачайте и положите в папку с приложением драйвер, с версией поддерживаемой вашим браузером:
```
https://sites.google.com/chromium.org/driver/
```


Clone and move to local repository:
```
git clone https://github.com/Elegantovich/TestYWeatherAPI/
```
Создайте файл `.env` командой
```
touch .env
```
и добавьте в него переменные окружения для работы с базой данных:
```
DJANGO_KEY=<your key> 
```
Create a virtual environment (win):
```
python -m venv venv
```
Activate a virtual environment:
```
source venv/Scripts/activate
```
Install dependencies from file requirements.txt:
```
pip install --upgrade pip
```
```
pip install requirements.txt
```
Create and run migrations:
```
python manage.py makemigrations
```
```
python manage.py migrate
```
Run the project:
```
python manage.py runserver
```

### Поддерживаемые endpoints:

| URL| Method | Description |
| ------ | ------ | ------ |
| http://127.0.0.1:8000/city/ | POST | {"city": "moscow"} |



## Notes
- Расположение драйвера по дефолту настроено в папке с проектом
- Результаты работы в виде ексель документа и БД будут находиться в папке с проектом

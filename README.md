# API_YaMDb

***

### Как запустить проект (windows):

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:InsomniaTSO/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install —upgrade pip
```

```
pip install -r requirements.txt
```

Перейти в папку с ``` manage.py ```:

```
cd api_yamdb
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

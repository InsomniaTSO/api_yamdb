# __Проект «API для Yamdb»__

## __Описание__:

API для оценки произведений (фильмов, книг, игр и т.п.).

## __Авторы__:

Матвей Бондаренко 
Назар Качура
Татьяна Манакова

### __Как запустить проект (windows)__:

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
python -m pip install --upgrade pip
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

### __Закачка данных из CSV__:

Запустить файл data_from_csv.py из папки с csv-файлами


## __Примеры запросов__:

Регистрация пользователя:

```
POST http://127.0.0.1:8000/api/v1/auth/signup/
{
"email": "string",
"username": "string"
}

```
На указанную почту придет код подтверждения.

Получение токена:

```
POST http://127.0.0.1:8000/api/v1/auth/token/
{
"confirmation_code": "string",
"username": "string"
}

```

Изменение/дополнение данных пользователя:

```
PATCH http://127.0.0.1:8000/api/v1/users/me/
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string"
}
```

Оставить отзыв с оценкой:

```
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
{
"text": "string",
"score": 1
}
```



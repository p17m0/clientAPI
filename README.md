# clientAPI

NO REDOC

В проекте есть 4 эндпоинта:


```
"http://127.0.0.1:8000/api/v1/upload_bills/"
```

```
"http://127.0.0.1:8000/api/v1/upload_client_org/"
```

```
"http://127.0.0.1:8000/api/v1/client_info/"
```

```
"http://127.0.0.1:8000/api/v1/bills/"
```


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:anotherUser2/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить сервер:

```
python3 manage.py runserver
```

Далее загрузить файл client_org.xlsx на соответствующий эндпоинт, после загрузить bills.xlsx соответственно.

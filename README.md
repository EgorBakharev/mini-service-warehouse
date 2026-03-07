# mini-service-warehouse
Создание товаров, складов и движение по складам.

## Содержание
- [Виртуальное окружение](#виртуальное-окружение)
- [Зависимость](#зависимость-)
- [Cервиса](#cервис)
- [Документация](#документация)
- [Тесты](#тесты)

## Виртуальное окружение
Создать виртуальное окружение (рекомендуется)
```sh
python -m venv venv
```
Активировать виртуальное окружение
Windows:
```sh
venv\Scripts\activate
```
Linux/Mac:
```sh
source venv/bin/activate
```

## Зависимость 
Устанавливаем
```sh
pip install -r requirements.txt
```

## Cервис
Запускаем
```sh
python -m uvicorn app.main:app
```
http://127.0.0.1:8000

## Документация
http://127.0.0.1:8000/docs

## Тесты
Запуск всех тестов
```sh
python -m pytest
```

Unit-тесты
```ch
python -m pytest .\tests\unit_test
```

Integration-тесты
```sh
python -m pytest .\tests\integration_test
```

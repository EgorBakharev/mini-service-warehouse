# mini-service-warehouse
Создание товаров, складов и движение по складам.

## Содержание
- [Виртуальное окружение](#виртуальное-окружение)
- [Зависимость](#зависимость-)
- [Cервиса](#cервис)
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
uvicorn app.main:app
```

## Тесты
Всех тестов
```sh
pytest
```

Unit-тесты
```ch
pytest .\tests\unit_test
```

Integration-тесты
```sh
pytest .\tests\integration_test
```
# GreenPy
Проект предназначен для выполнения файлов Jupyter Notebook .ipynb на удалённом сервере. Внутри проекта загружены наиболее популярные библиотеки для обработки данных (numpy, pandas, scipy), 
построения моделей (scikit-learn), визуализации (matplotlib, seaborn), организации параллельных вычислений (dask, numba). 

Исполняемый файл передается в формате JSON в теле HTTP-запроса. Пример запроса:
```python
{
    "uuid": "uuid",
    "envname": "uuid.env",
    "env": {
        "DATA_PATH": "uuid/DATA.csv",
        "RESULT_PATH": "uuid/RESULT.csv",
        "TEST": "1.txt"
    },
    "notebook": {
        "cells": ...
    }
}
```
Файлы, используемые при выполнении ноутбука, помещаются в рабочую папку на компьютере пользователя, которая
монтируется к серверу. Путь к исходным и полученным файлам передается по ключу *env* в запросе.

Для передачи паметров используется библиотека [dotenv](https://github.com/theskumar/python-dotenv).  
В Jupyter Notebook должно быть загружено расширение `%load_ext dotenv`.  
Обращение к переменным в нотбуке через `os.getenv('DATA')`. 

Пример вызова сервиса:  
` curl -d "{\"uuid\":\"55b502b6-61b4-d893-8395-b97ba7aff603\",\"env\":{\"DATA\":\"1\"},\"envname\":\"55b502b6-61b4-d893-8395-b97ba7aff603.env\",\"notebook\":{\"cells\":[{\"cell_type\":\"code\",\ "execution_count\":null,\"metadata\":{},\"outputs\":[],\"source\":[\"%load_ext dotenv\n\",\"%dotenv -o 55b502b6-61b4-d893-8395-b97ba7aff603.env\n\",\"import os\"]},{\"cell_type\":\"code\",\"execution_count\":null,\"metadata\":{},\"outputs\ ":[],\"source\":[\"int(os.getenv('DATA')) + 1\"]}],\"metadata\":{\"kernelspec\":{\"display_name\":\"Python 3\",\"language\":\"python\",\"name\":\"python3\"},\"language_info\":{\"codemirror_mode\":{\"name\":\"ipython\",\"version\":3},\"file _extension\":\".py\",\"mimetype\":\"text/x-python\",\"name\":\"python\",\"nbconvert_exporter\":\"python\",\"pygments_lexer\":\"ipython3\",\"version\":\"3.7.3\"}},\"nbformat\":4,\"nbformat_minor\":2}}" -H "Content-Type: application/json" -X  POST http://192.168.0.104:8787/api/execute`

Результат выполнения ноутбука приходит в ответе на запрос в JSON: выполненный ноутбук или
информация об ошибке.  
Формат ответа:
```json
{
  "error": null,
  "notebook": {
    "cells": ...
  }
}
```

## Приступая к работе
Перед началом работы необходимо смонтировать рабочую папку проекта на локальном компьютере клиента к серверу. 
В этой папке необходимо разместить файлы для выполнения Jupyter Notebook. Пример монтирования:

`sudo mount -t cifs -o file_mode=0777,dir_mode=0777 //192.168.0.173/python_share /home/infobot/apps/greenpy/mnt`

Примечание: необходимо смонитировать папку вне зависимости от того, использует ли ноутбук внешние файлы.

Далее необходимо указать путь к смонтированной папке. В файле *docker-compose.yml* в разделе volumes заменить путь 
источника (слева) на путь к папке. Для примера выше: */home/infobot/apps/greenpy/mnt*:

### Установка
Для разработчиков достаточно импротировать проект в одну из IDE для Python. Для непосредственного использования
проект предусматривает сборку контейнера Docker для запуска на удалённом сервере. Подробнее об установке 
проекта см. в разделе "Развёртывание".

### Развёртывание
Для внедрения на сервер используется контейнеризация Docker. Для запуска импортированного образа необходимо запустить 
менеджер пакетов docker-compose в директории файла *docker-compose.yml*:

    docker-compose up

По умолчанию, для обращения к контейнеру используется порт 8787. Изменить порт можно в файле *docker-compose.yml*.

## Создано с помощью
* Flask - фреймворк веб-приложения
* PyCharm - разработка проекта
* Docker - контейнеризация проекта
* Docker-compose - менеджер контейнеров
* Jupyter Notebook - выполнение пользовательского кода
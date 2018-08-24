# TechOps.logparser

Тестовое задание по поиску строки в логе на удаленном сервере и вывод -100/+100 строк от него

## Постановка

Пользователь вводит ip-адрес, маску названия лога и числовой идентификатор, по которому нужно найти информацию в логе на сервере. Необходимо написать функцию, которая по входным данным найдёт в логе:

1. Строку в логе с идентификатором.
2. Выведет +100 и -100 строк от этого идентификатора.

**Дополнительные данные**: можно использовать абстрактную функцию def auth_data(ip-адрес) , которая возвращает по IP адресу пару login/password для аутентификации на сервере. 

Задание необходимо реализовать без использования команды grep. Нужно использовать именно python.

## Описание проекта

Финальный метод, который является точкой входа в приложение расположен в модуле **src/getlog.py**. Метод пользуется двумя большими абстракциями.

1. класс sftp.Sftp - Подключение к серверу по SFTP поверх SSH. Дополнительно содержит методы поиска файлов по Unix-wildcards.
2. класс fileexplorer.FileExplorer - обобщенная обертка поверх file-like объектов, которая предоставляет произвольный построчный доступ к файлу. Оффсеты начала считанных/проитерированных строк кешируются. Это дает возможность быстро переставлять курсор чтения, на уже прочитанные строки.

На оба класса написаны тесты. Тесты **test_fileexplorer.py** можно запускать локально. Тесты **test_sftp.py** требуют подключения к серверу, на котором где-то расположены копии логов из папки **testdata**. 

В папке **testdata** лежат файлы логов. Текст для логов сгенерирован методом **tools.log_text_generator**. Каждая запись в логах строиться по формату: `<date> <id> <message`, где **id** - уникальное в пределах файла числовое ID. Цифр в нем много, так что велика вероятность что многие ID будут уникальны в пределах всего набора логов.

Как испольняется метод поиска **getlog.print_200_lines_of_log**:

1. модуль подключается к указанному серверу, с указанной аутентификацией 
2. находит папку с логами
3. находит в ней все файлы соотвествующие маске
4. перебирает все найденные файлы в поисках строки, содержащую ID
5. выводит 100 предшествующих строк, саму строку, 100 последующих строк (выходы за границы файла обрабатываются)

## Установка

Требования:

 - Python >= 3.6.5
 - pip >= 9.0.3

```sh
git clone https://mirakulus@bitbucket.org/mirakulus/techops.logparser.git
cd techops.logparser
pip install -r requirements.txt
python src/getlog.py --help
```

## Запуск

Модуль **getlog.py** имеет интерфейс командной строки.

Пример запуска:

```sh
cd $repo_path
python src/getlog.py -s 192.168.1.5 -p 2222 --user user --pass pwd -d /var/log/techops -m *.log -i 672330495
```

По аргументу `--help` можно получить справку.
Последний вывод справки:

```sh
usage: getlog.py [-h] -s SERVER [-p PORT] [-u USER] [--pass PASS] -d DIR -m
                 MASK -i ID

Find line in remote log and print 100 lines up and down around it

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        Server to connect
  -p PORT, --port PORT  Port for server to connect
  -u USER, --user USER  User for server connection
  --pass PASS           Password for server connection
  -d DIR, --dir DIR     Directory storing logs you wish to explore
  -m MASK, --mask MASK  Unix-style wildcards for searching logs. Examples =
                        '*.log', 'logs*', '*3*'
  -i ID, --id ID        Id-string you wish to search
```


*В коде осталось автоматическое получение аутентификационных данных по имени сервера. Код расположен в **sftp.py** в классе **AuthData** в статическом методе **get_auth_data(server)**. В данный момент, он отдает только логин/пароль для моего дев-сервера. Метод вызывается, если отсутсвует аргумент --user*


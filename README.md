# TechOps.logparser

Тестовое задание по парсингу лога с удаленного сервера

## Постановка

Пользователь вводит ip-адрес, маску названия лога и числовой идентификатор, по которому нужно найти информацию в логе на сервере. Необходимо написать функцию, которая по входным данным найдёт в логе:

1. Строку в логе с идентификатором.
2. Выведет +100 и -100 строк от этого идентификатора.

**Дополнительные данные**: можно использовать абстрактную функцию def auth_data(ip-адрес) , которая возвращает по IP адресу пару login/password для аутентификации на сервере. 

Задание необходимо реализовать без использования команды grep. Нужно использовать именно python.

## Описание проекта
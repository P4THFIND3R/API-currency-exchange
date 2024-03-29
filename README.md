# API Currency Exchange

## Развертывание

В целом, с вашей стороны никаких настроек не требуется.
Развернуть docker-compose можно следующей командой, для этого необходимо находиться в корне проекта:
``` bash
docker compose up
```
Приложение будет доступно на порту 9999, модуль документации /docs открыт.

## Структура и описание приложения
API позволяет получать данные о текущих валютных курсах, имеет контроль аутентификации и авторизации на основе JWT, данные хранятся на Postgresql.

Приложение включает в себя следующие модули:
- Модуль аутентификации и авторизации на основе JWT, и содержит в себе функции генерации и выдачи access & refresh токенов, учет пользовательских сессий, автоматическое обновление токенов в случае истечения их срока действия. 
  При разработке модуля наткнулся на очень хорошую статью ->
  https://gist.github.com/zmts/802dc9c3510d79fd40f9dc38a12bccfc
  С точки зрения пользователя принцип работы следующий:
	-  Аутентификация;
		- Пользователь через форму вводит логин+пароль;
			- Для пользователя генерируется access token:
			- Для пользователя генерируется refresh token:
				- Проверить количество текущих сессий пользователя. Если количество превышает 5, аннулируем все предыдущие сессии.
			- В пользовательских куках устанавливаются httpOnly куки access и refresh токена. 
	- Авторизация;
			У каждого защищенному роута будет определена зависимость от проверки действительности access_token пользователя, а так-же соответствие тому, что роль в токене равна или выше чем закрепленная роль в роуте.
	-  Обновление токенов.
		В чем суть. Пользователю выдаются access и refresh токены, время жизни которых соответственно 30 минут и 30 дней. После того, как у access токен истек срок годности, мы автоматически обновляем его при помощи refresh токена.
		В свою очередь refresh токен обновляется вместе с access.
		- Реализовать проверку валидности refresh токена;
			- Проверить наличие сессии по указанному id;
			- Проверить не истек ли срок годности;
			- Сравнить fingerprint в сессии и fingerprint пользователя. В случае невалидности аннулируем токен и перенаправляем на страницу авторизации.
		- Создать новый access token, refresh token;
			- Обновить данные Session, User_session.
		- Записать токены в httpOnly куки.
- Модуль работы с внешним API, который предоставляет данные о курсах валют, позволяет конвертировать валюты. Каждый endpoint работы с валютами защищен и для использования требует авторизацию при помощи JWT (access токена).
# YandexApiProject
Проект: "Планировщик"\
— Идея проекта довольно проста: Сайт с системой регистрации и авторизации пользователей, системой друзей, возможностью создания мероприятия пользователем, оно может быть открытым, что в свою очередь дает возможность присоединиться к нему любому желающему, и закрытым, попасть в которое можно лишь, если этого захочет его организатор(так же нужно быть его другом для этого). Так же создатель мероприятия имеет возможность удалить его или редактировать, исключать участников.\
Проект размещен по ссылке: https://yl-flask-project.herokuapp.com \
База данных имеет пять сущностей.\
User с полями: \
—id(int)\
—name(string) имя\
—surname(string) фамилия\
—date_of_birth(DateTime) дата рождения\
—email(string, unique=True)\
—hashed_password(string) хешированный пароль\
—city_from(string) город проживания\
—country_from(int) страна проживания\
—friends(string) id пользователей через запятую\
Скрытые поля: \
—tasks(list), хранит сущности класса Task, добавление сущности изменяет таблица task_to_user \
Методы: \
—set_password(password) устанавливает хешированную переданную строку значением поля hashed_password \
-check_password(password) возвращает True/False в зависимости от совпадения переданной строки с расхешированным паролем \
—get_friends_list возвращает список id(int) друзей \
—set_friends(array) принимает список из id, превращает его в строку с разделителем ", " и устанавливает созданную строку значением поля friends

api запросы для User: \
Передача верного api_key по ключу 'api_key' обязательна для всех запросов.

get: \
—Получить пользователя с определенным id. URL для запроса: http/yl-flask-project.herokuapp.com/api/users/id(int) \
—Получить всех пользователей. URL для запроса: http/yl-flask-project.herokuapp.com/api/users

delete: \
—Удалить пользователя с определенным id. URL для запроса: http/yl-flask-project.herokuapp.com/api/users/id(int)

post: \
—Добавить пользователя. URL для запроса: http/yl-flask-project.herokuapp.com/api/users \
Для данного запроса обязательна передача параметров по ключам: \
name ; surname ; date_of_birth ; email ; password ; city_from ; country_from ; friends

Пример значения полей по ключам: \
"name":'Name' \
"surname":'Surname' \
"date_of_birth":'2001-01-01' \
"email":'example@domen.com' \
"password":'password' \
"city_from":'London' \
"country_from":'2'(Узнать id стран можно с помощью api запроса к country) \
"friends":[1, 2, 3]

—Изменить данные пользователя. URL для запроса: http/yl-flask-project.herokuapp.com/api/users \
Для данного запроса обязательная передача значения по ключу: id \
и, как минимум, одного поля из данного списка: \
name ; surname ; date_of_birth ; email ; password ; city_from ; country_from ; friends

Пример значения полей по ключам: \
"id":1
"name":'Name' \
"surname":'Surname' \
"date_of_birth":'2001-01-01' \
"email":'example@domen.com' \
"password":'password' \
"city_from":'London' \
"country_from":'2'(Узнать id стран можно с помощью api запроса к country) \
"friends":[1, 2, 3]


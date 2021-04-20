# YandexApiProject
Проект: "Планировщик"\
— Идея проекта довольно проста: Сайт с системой регистрации и авторизации пользователей, системой друзей, возможностью создания мероприятия пользователем, оно может быть открытым, что в свою очередь дает возможность присоединиться к нему любому желающему, и закрытым, попасть в которое можно лишь, если этого захочет его организатор(так же нужно быть его другом для этого). Так же создатель мероприятия имеет возможность удалить его или редактировать, исключать участников.\
Проект размещен по ссылке: https://yl-flask-project.herokuapp.com \
База данных имеет пять сущностей.\
————————————————————— \
User с полями: \
—id(int)\
—name(string) имя\
—surname(string) фамилия\
—date_of_birth(DateTime) дата рождения(год-месяц-день)\
—email(string, unique=True)\
—hashed_password(string) хешированный пароль\
—city_from(string) город проживания\
—country_from(int) id страны проживания\
—friends(string) id пользователей(друзей) запятую с пробелом

Скрытые поля: \
—tasks(list), хранит сущности класса Task, добавление сущности изменяет таблицу task_to_user \
—creator, необходима для связи с полем creator в сущности класса Task

Методы: \
—set_password(password) устанавливает хешированную переданную строку значением поля hashed_password \
—check_password(password) возвращает True/False в зависимости от совпадения переданной строки с расхешированным паролем \
—get_friends_list возвращает список id(int) друзей \
—set_friends(array) принимает список из id, превращает его в строку с разделителем ", " и устанавливает созданную строку значением поля friends

api запросы для User: \
Передача верного api_key по ключу 'api_key' обязательна для всех запросов.

get: \
—Получить пользователя с определенным id. URL для запроса: https://yl-flask-project.herokuapp.com/api/users/id(int) \
—Получить всех пользователей. URL для запроса: https://yl-flask-project.herokuapp.com/api/users

delete: \
—Удалить пользователя с определенным id. URL для запроса: https://yl-flask-project.herokuapp.com/api/users/id(int)

post: \
—Добавить пользователя. URL для запроса: https://yl-flask-project.herokuapp.com/api/users \
Для данного запроса обязательна передача параметров по ключам: \
name ; surname ; date_of_birth ; email ; password ; city_from ; country_from ; friends

Пример значения полей по ключам: \
"name":'Name' \
"surname":'Surname' \
"date_of_birth":'2001-01-01' \
"email":'example@domen.com' \
"password":'password' \
"city_from":'London' \
"country_from":2(Узнать id стран можно с помощью api запроса к country) \
"friends":[1, 2, 3]

—Изменить данные пользователя. URL для запроса: https://yl-flask-project.herokuapp.com/api/users \
Для данного запроса обязательная передача значения по ключу: id \
и, как минимум, одного поля из данного списка: \
name ; surname ; date_of_birth ; email ; password ; city_from ; country_from ; friends

Пример значения полей по ключам: \
"id":1 \
"name":'Name' \
"surname":'Surname' \
"date_of_birth":'2001-01-01' \
"email":'example@domen.com' \
"password":'password' \
"city_from":'London' \
"country_from":2 (Узнать id стран можно с помощью api запроса к country) \
"friends":[1, 2, 3]

—————————————————————

Task с полями: \
—id(int) \
—creator_id(int) id создателя мероприятия\
—type(int) id типа мероприятия\
—title(string) название\
—description(string) описание\
—participating(string) id пользователей(участвующих) через запятую с пробелом(без id создателя)\
—date(DateTime) дата проведения(год-месяц-день час:минуты)\
—address(string) адресс\
—country(int) id страны проведения\
—is_private(bool) Приватное(Личное) ли мероприятие?\
—is_address_displayed(bool) Добавить картинку с адресом с карты? 

Методы:
—get_participates_list возвращает список id(int) участвующих(без creator_id) \
—set_participates(array) принимает список из id, превращает его в строку с разделителем ", " и устанавливает созданную строку значением поля participating

api запросы для Task: \
Передача верного api_key по ключу 'api_key' обязательна для всех запросов.

get: \
—Получить мероприятие с определенным id. URL для запроса: https://yl-flask-project.herokuapp.com/api/tasks/id(int) \
—Получить все мероприятия. URL для запроса: https://yl-flask-project.herokuapp.com/api/tasks

delete: \
—Удалить мероприятие с определенным id. URL для запроса: https://yl-flask-project.herokuapp.com/api/tasks/id(int)

post: \
—Добавить мероприятие. URL для запроса: https://yl-flask-project.herokuapp.com/api/tasks \
Для данного запроса обязательна передача параметров по ключам: \
creator_id ; type ; title ; description ; participating ; date ; address ; country ; is_private; is_address_displayed 

Пример значения полей по ключам: \
—"creator_id":1 \
—"type":1 (Узнать id типов можно с помощью api запроса к type)\
—"title":'Title' \
—"description":'Description \
—"participating":[2,3] \
—"date":'2000-01-01 16:00'\
—"address":'address' \
—"country":1 (Узнать id стран можно с помощью api запроса к country)\
—"is_private":True \
—"is_address_displayed":True

—Изменить данные мероприятия. URL для запроса: https://yl-flask-project.herokuapp.com/api/tasks \
Для данного запроса обязательная передача значения по ключу: id \
и, как минимум, одного поля из данного списка: \
creator_id ; type ; title ; description ; participating ; date ; address ; country ; is_private; is_address_displayed 

Пример значения полей по ключам: \
—"id":1 \
—"creator_id":1 \
—"type":1 (Узнать id типов можно с помощью api запроса к type)\
—"title":'Title' \
—"description":'Description \
—"participating":[2,3] \
—"date":'2000-01-01 16:00'\
—"address":'address' \
—"country":1 (Узнать id стран можно с помощью api запроса к country)\
—"is_private":True \
—"is_address_displayed":True

—————————————————————

Country с полями: \
—id(int) \
—name(string, unique=True) название страны

Скрытые поля: \
—tasks(list), хранит сущности класса Task, добавление сущности изменяет таблицу task_to_country 

api запросы для Country: \
Передача верного api_key по ключу 'api_key' обязательна для всех запросов.

get: \
—Получить страну с определенным id. URL для запроса: https://yl-flask-project.herokuapp.com/api/countries/id(int) \
—Получить все страны. URL для запроса: https://yl-flask-project.herokuapp.com/api/countries

delete: \
—Удалить страну с определенным id. URL для запроса: https://yl-flask-project.herokuapp.com/api/countries/id(int)

post: \
—Добавить страну. URL для запроса: https://yl-flask-project.herokuapp.com/api/countries \
Для данного запроса обязательна передача параметров по ключам: \
name ; 

Пример значения полей по ключам: \
"name":'Name'

—Изменить данные страны. URL для запроса: https://yl-flask-project.herokuapp.com/api/countries \
Для данного запроса обязательная передача значения по ключу: id ; name

Пример значения полей по ключам: \
"id":1 \
"name":'Name'

—————————————————————

Type с полями: \
—id(int) \
—title(string, unique=True) название типа

Скрытые поля: \
—tasks(list), хранит сущности класса Task, добавление сущности изменяет таблицу task_to_type 

api запросы для Type: \
Передача верного api_key по ключу 'api_key' обязательна для всех запросов.

get: \
—Получить тип с определенным id. URL для запроса: https://yl-flask-project.herokuapp.com/api/types/id(int) \
—Получить все типы. URL для запроса: https://yl-flask-project.herokuapp.com/api/types

delete: \
—Удалить тип с определенным id. URL для запроса: https://yl-flask-project.herokuapp.com/api/types/id(int)

post: \
—Добавить тип. URL для запроса: https://yl-flask-project.herokuapp.com/api/types \
Для данного запроса обязательна передача параметров по ключам: \
title ; 

Пример значения полей по ключам: \
"title":'Title'

—Изменить данные типа. URL для запроса: https://yl-flask-project.herokuapp.com/api/types \
Для данного запроса обязательная передача значения по ключу: id ; title

Пример значения полей по ключам: \
"id":1 \
"title":'Title'

—————————————————————

FriendRequest с полями: \
—id(int) \
—sended_by(int) id отправителя заявки в друзья \
—received_by(int) id того, кому отправили заявку в друзья

api запросы для FriendRequest: \
Передача верного api_key по ключу 'api_key' обязательна для всех запросов.

get: \
—Получить запрос в друзья с определенным id. URL для запроса: https://yl-flask-project.herokuapp.com/api/friend_requests/id(int) \
—Получить все запросы в друзья. URL для запроса: https://yl-flask-project.herokuapp.com/api/friend_requests

delete: \
—Удалить запрос в друзья с определенным id. URL для запроса: https://yl-flask-project.herokuapp.com/api/friend_requests/id(int)

post: \
—Добавить запрос в друзья. URL для запроса: https://yl-flask-project.herokuapp.com/api/friend_requests \
Для данного запроса обязательна передача параметров по ключам: \
sended_by ; received_by

Пример значения полей по ключам: \
"sended_by":1 \
"received_by":2

—Изменить данные запроса в друзья. URL для запроса: https://yl-flask-project.herokuapp.com/api/friend_requests \
Для данного запроса обязательная передача значения по ключу: id \
и, как минимум, одного поля из данного списка: \
sended_by ; received_by

Пример значения полей по ключам: \
"id":1 \
"sended_by":1 \
"received_by":2

—————————————————————

Для всех сущностей есть тесты api запросов. Тесты настроены под бд, заполненную лишь через файлы set_all_countries.py и set_all_types.py


—set_all_countries.py \
Добавляет в БД все страны, каждая страна с новой строки, из файла countries.txt

—set_all_types.py \
Добавляет в БД все типы, каждый тип с новой строки, из файла types.txt

—————————————————————

Для полей по ключам в post api запросах есть свои ограничения:

Передаваемые данные должны соответсвовать типам полей.

User: \
—email: Строка должна содержать валидный адрес, который ранее не использовался, похожий на: "example@domen.com" \
—date_of_birth: Строка должна содержать валидный тип даты, похожий на: "2000-01-01" \
—country_from: id страны должно существовать в БД \
—friends: id пользователей должны существовать в БД

Task: \
—date: Cтрока должна содержать валидный тип даты, похожий на: "2000-01-01 16:00" \
—creator_id: id пользователя должны существовать в БД \
—participating: id пользователей должны существовать в БД ; creator_id не может находиться в этом списке \
—country: id страны должно существовать в БД \
—type: id типа должно существовать в БД

Country: \
—name: Строка должна содержать название страны, которое ранее не использовалось в таблице countries

Type: \
—title: Строка должна содержать название типа, которое ранее не использовалось в таблице types

FriendRequest: \
—sended_by не может быть равно received_by \
—В таблице friendrequests не должен существовать запрос, который похож на создаваемый, тоесть запрос, который отличен лишь тем, что sended_by и received_by поменяны местами, не может быть создан

Примечание: \
—При несоблюдении перечисленных ограничений будет возвращено сообщение, которое будет содержать информацию об ошибке

Другое: \
—При непрерывной работе сервера, каждый день будут удаляться мероприятия, дата проведения которых была более недели назад \
—При запуске сервера в файл current_time_zone.txt записывается текущий часовой пояс машины, с которой был произведен запуск. Данный часовой пояс будет отображен на странице редактирования и создания мероприятия
—Валидный api ключ находиться в файле current_api_key.txt
 

from requests import get,post,delete,patch
cur_api_key = open('../data/current_api_key.txt', 'r').readline()
post('http://localhost:80/api/users',json={'api_key':cur_api_key,
                                                 'name':'Остап',
                                                 'surname':'Кормильцев',
                                                 'date_of_birth':'2003-01-04',
                                                 'email':'error1number404@gmail.com',
                                                 'password':'password',
                                                 'city_from':'Барнаул',
                                                 'country_from':180,
                                                 'friends':[]})
post('http://localhost:80/api/users',json={'api_key':cur_api_key,
                                                 'name':'Алексей',
                                                 'surname':'Шишкин',
                                                 'date_of_birth':'2002-10-17',
                                                 'email':'aa@gmail.com',
                                                 'password':'password',
                                                 'city_from':'Нижний Новгород',
                                                 'country_from':180,
                                                 'friends':[]})
post('http://localhost:80/api/users', json={'api_key': cur_api_key,
                                            'name': 'Андрей',
                                            'surname': 'Дьяков',
                                            'date_of_birth': '2002-09-21',
                                            'email': 'bb@gmail.com',
                                            'password': 'password',
                                            'city_from': 'Севастополь',
                                            'country_from': 180,
                                            'friends': []})# создадим пользователей для тестов
print(post('http://localhost:80/api/friend_requests',json={'sended_by':1,
                                                           'received_by':2}).json()) # нет api ключа
print(post('http://localhost:80/api/friend_requests',json={'api_key':'wrong_api_key',
                                                 'sended_by':1,
                                                 'received_by':2}).json()) # неправильный api ключ
print(post('http://localhost:80/api/friend_requests',json={'api_key':cur_api_key,
                                                 'sended_by':1,
                                                 'received_by':1}).json()) # получатель равен отправителю
print(post('http://localhost:80/api/friend_requests',json={'api_key':cur_api_key,
                                                 'sended_by':5,
                                                 'received_by':1}).json()) # пользователь не существует(sended_by)
print(post('http://localhost:80/api/friend_requests',json={'api_key':cur_api_key,
                                                 'sended_by':1,
                                                 'received_by':5}).json()) # пользователь не существует(received_by)
print(post('http://localhost:80/api/friend_requests',json={'api_key':cur_api_key,
                                                 'sended_by':1}).json()) # переданы не все поля на создание
print(post('http://localhost:80/api/friend_requests',json={'api_key':cur_api_key,
                                                 'sended_by':1,
                                                 'received_by':2}).json()) # все верно
print(post('http://localhost:80/api/friend_requests',json={'api_key':cur_api_key,
                                                 'sended_by':1,
                                                 'received_by':2}).json()) # такой запрос уже существует(или ему обратный)
print(post('http://localhost:80/api/friend_requests',json={'api_key':cur_api_key,
                                                 'sended_by':2,
                                                 'received_by':1}).json()) # такой запрос уже существует(или ему обратный)
print(post('http://localhost:80/api/friend_requests',json={'api_key':cur_api_key,
                                                 'sended_by':1,
                                                 'received_by':3}).json()) # все верно
print(patch('http://localhost:80/api/friend_requests',json={'api_key':cur_api_key,
                                                  'id':2,
                                                  'sended_by':1,
                                                  'received_by':2}).json()) # такой запрос уже существует(или ему обратный)
print(patch('http://localhost:80/api/friend_requests',json={'api_key':cur_api_key,
                                                  'id':2,
                                                  'received_by':2}).json()) # такой запрос уже существует(или ему обратный)
print(patch('http://localhost:80/api/friend_requests',json={'api_key':cur_api_key,
                                                  'id':2}).json()) # нет полей для редактирования
print(patch('http://localhost:80/api/friend_requests',json={'api_key':cur_api_key,
                                                  'received_by':2}).json()) # нет id
print(get('http://localhost:80/api/friend_requests/1',json={'api_key':cur_api_key}).json()) # все верно
print(get('http://localhost:80/api/friend_requests',json={'api_key':cur_api_key}).json()) # все верно
print(delete('http://localhost:80/api/friend_requests/1',json={'api_key':cur_api_key}).json()) # все верно
print(delete('http://localhost:80/api/friend_requests/2',json={'api_key':cur_api_key}).json()) # все верно
delete('http://localhost:80/api/users/1', json={'api_key':cur_api_key}) # удаляем созданных для тестов пользователей
delete('http://localhost:80/api/users/2', json={'api_key':cur_api_key})
delete('http://localhost:80/api/users/3', json={'api_key':cur_api_key})

from requests import get,post,delete,patch
cur_api_key = open('../data/current_api_key.txt', 'r').readline()
print(post('http://localhost:80/api/users',json={'name':'Остап',
                                                 'surname':'Кормильцев',
                                                 'date_of_birth':'2003-01-04',
                                                 'email':'error1number404@gmail.com',
                                                 'password':'password',
                                                 'city_from':'Барнаул',
                                                 'country_from':180,
                                                 'friends':[]}).json()) # нет api ключа
print(post('http://localhost:80/api/users',json={'api_key':'wrong_key',
                                                 'name':'Остап',
                                                 'surname':'Кормильцев',
                                                 'date_of_birth':'2003-01-04',
                                                 'email':'error1number404@gmail.com',
                                                 'password':'password',
                                                 'city_from':'Барнаул',
                                                 'country_from':180,
                                                 'friends':[]}).json()) # неверный api ключ
print(post('http://localhost:80/api/users',json={'api_key':cur_api_key,
                                                 'name':'Остап',
                                                 'surname':'Кормильцев',
                                                 'date_of_birth':'01.04.2003',
                                                 'email':'error1number404@gmail.com',
                                                 'password':'password',
                                                 'city_from':'Барнаул',
                                                 'country_from':180,
                                                 'friends':[]}).json()) # неправильный формат даты
print(post('http://localhost:80/api/users',json={'api_key':cur_api_key,
                                                 'name':'Остап',
                                                 'surname':'Кормильцев',
                                                 'date_of_birth':'2003-01-04',
                                                 'email':'error1number404gmail.com',
                                                 'password':'password',
                                                 'city_from':'Барнаул',
                                                 'country_from':180,
                                                 'friends':[]}).json()) # неправильный email
print(post('http://localhost:80/api/users',json={'api_key':cur_api_key,
                                                 'name':'Остап',
                                                 'surname':'Кормильцев',
                                                 'date_of_birth':'2003-01-04',
                                                 'email':'error1number404@gmail.com',
                                                 'friends':[]}).json()) # переданы не все поля на создание
print(post('http://localhost:80/api/users',json={'api_key':cur_api_key,
                                                 'name':'Остап',
                                                 'surname':'Кормильцев',
                                                 'date_of_birth':'2003-01-04',
                                                 'email':'error1number404@gmail.com',
                                                 'password':'password',
                                                 'city_from':'Барнаул',
                                                 'country_from':180,
                                                 'friends':[]}).json()) # все верно
print(post('http://localhost:80/api/users',json={'api_key':cur_api_key,
                                                 'name':'Алексей',
                                                 'surname':'Шишкин',
                                                 'date_of_birth':'2002-10-17',
                                                 'email':'error1number404@gmail.com',
                                                 'password':'password',
                                                 'city_from':'Нижний Новгород',
                                                 'country_from':180,
                                                 'friends':[]}).json()) # повторение email
print(post('http://localhost:80/api/users',json={'api_key':cur_api_key,
                                                 'name':'Алексей',
                                                 'surname':'Шишкин',
                                                 'date_of_birth':'2002-10-17',
                                                 'email':'aa@gmail.com',
                                                 'password':'password',
                                                 'city_from':'Нижний Новгород',
                                                 'country_from':180,
                                                 'friends':[]}).json()) # все верно
print(patch('http://localhost:80/api/users',json={'api_key':cur_api_key,
                                                 'friends':[2]}).json()) # нет id
print(patch('http://localhost:80/api/users',json={'api_key':cur_api_key,
                                                 'id':1}).json()) # нет полей для редактирования
print(patch('http://localhost:80/api/users',json={'api_key':cur_api_key,
                                                 'id':1,
                                                 'friends':[2]}).json()) # все верно
print(get('http://localhost:80/api/users/1', json={'api_key':cur_api_key}).json())# все верно
print(get('http://localhost:80/api/users', json={'api_key':cur_api_key}).json())# все верно
print(delete('http://localhost:80/api/users/1', json={'api_key':cur_api_key}).json())# все верно
print(delete('http://localhost:80/api/users/2', json={'api_key':cur_api_key}).json())# все верно

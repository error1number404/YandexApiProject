from requests import get,post,delete,patch
cur_api_key = open('../data/current_api_key.txt', 'r').readline()
print(post('http://localhost:80/api/countries',json={'name':'new country'}).json()) # нет api ключа
print(post('http://localhost:80/api/countries',json={'api_key':'wrong_api_key',
                                                     'name':'new country'}).json()) # неверный api ключ
print(post('http://localhost:80/api/countries',json={'api_key':cur_api_key,
                                                     'name':'old country'}).json()) # все верно
print(post('http://localhost:80/api/countries',json={'api_key':cur_api_key,
                                                     'name':'new country'}).json()) # все верно
print(post('http://localhost:80/api/countries',json={'api_key':cur_api_key,
                                                     'name':'new country'}).json()) # такая страна уже существует
print(patch('http://localhost:80/api/countries',json={'api_key':cur_api_key,
                                                      'id':2,
                                                     'name':'old country'}).json()) # такая страна уже существует
print(patch('http://localhost:80/api/countries',json={'api_key':cur_api_key,
                                                     'name':'old country'}).json()) # нет id
print(patch('http://localhost:80/api/countries',json={'api_key':cur_api_key,
                                                      'id':2}).json()) # нет полей для редактирования
print(get('http://localhost:80/api/countries/1',json={'api_key':cur_api_key}).json()) # все верно
print(get('http://localhost:80/api/countries',json={'api_key':cur_api_key}).json()) # все верно
print(delete('http://localhost:80/api/countries/2',json={'api_key':cur_api_key}).json()) # все верно
print(delete('http://localhost:80/api/countries/1',json={'api_key':cur_api_key}).json()) # последняя страна, нельзя удалить т.к повлечен за собой нарушение остальных таблиц


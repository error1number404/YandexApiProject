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
                                                      'id':243,
                                                     'name':'old country'}).json()) # такая страна уже существует
print(patch('http://localhost:80/api/countries',json={'api_key':cur_api_key,
                                                     'name':'old country'}).json()) # нет id
print(patch('http://localhost:80/api/countries',json={'api_key':cur_api_key,
                                                      'id':243}).json()) # нет полей для редактирования
print(get('http://localhost:80/api/countries/242',json={'api_key':cur_api_key}).json()) # все верно
print(get('http://localhost:80/api/countries',json={'api_key':cur_api_key}).json()) # все верно
print(delete('http://localhost:80/api/countries/242',json={'api_key':cur_api_key}).json()) # все верно
print(delete('http://localhost:80/api/countries/243',json={'api_key':cur_api_key}).json()) # все верно

# если очистить таблицу countries,а затем выполнить эти запросы, то при попытке удаления последнего элемента выпадет ошибка, т.к нельзя удалить последнюю сущность. Удаление последней сущности в таблице countries сломает остальные таблицы.
# print(post('http://localhost:80/api/countries',json={'api_key':cur_api_key,
#                                                      'name':'old country'}).json())
# print(delete('http://localhost:80/api/countries/1',json={'api_key':cur_api_key}).json()) # здесь будет ошибка
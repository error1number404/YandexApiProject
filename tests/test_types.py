from requests import get,post,delete,patch
cur_api_key = open('../data/current_api_key.txt', 'r').readline()
print(post('http://localhost:80/api/types',json={'name':'new type'}).json()) # нет api ключа
print(post('http://localhost:80/api/types',json={'api_key':'wrong_api_key',
                                                     'title':'new type'}).json()) # неверный api ключ
print(post('http://localhost:80/api/types',json={'api_key':cur_api_key,
                                                     'title':'old type'}).json()) # все верно
print(post('http://localhost:80/api/types',json={'api_key':cur_api_key,
                                                     'title':'new type'}).json()) # все верно
print(post('http://localhost:80/api/types',json={'api_key':cur_api_key,
                                                     'title':'new type'}).json()) # такой тип уже существует
print(patch('http://localhost:80/api/types',json={'api_key':cur_api_key,
                                                      'id':33,
                                                     'title':'old type'}).json()) # такой тип уже существует
print(patch('http://localhost:80/api/types',json={'api_key':cur_api_key,
                                                     'title':'old type'}).json()) # нет id
print(patch('http://localhost:80/api/types',json={'api_key':cur_api_key,
                                                      'id':33}).json()) # нет полей для редактирования
print(get('http://localhost:80/api/types/32',json={'api_key':cur_api_key}).json()) # все верно
print(get('http://localhost:80/api/types',json={'api_key':cur_api_key}).json()) # все верно
print(delete('http://localhost:80/api/types/32',json={'api_key':cur_api_key}).json()) # все верно
print(delete('http://localhost:80/api/types/33',json={'api_key':cur_api_key}).json()) # все верно


# если очистить таблицу types,а затем выполнить эти запросы, то при попытке удаления последнего элемента выпадет ошибка, т.к нельзя удалить последнюю сущность. Удаление последней сущности в таблице types сломает остальные таблицы.
# print(post('http://localhost:80/api/types',json={'api_key':cur_api_key,
#                                                      'title':'old type'}).json())
# print(delete('http://localhost:80/api/types/1',json={'api_key':cur_api_key}).json()) # здесь будет ошибка
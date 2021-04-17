import requests
def get_map_picture(id,address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": address,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    address_ll = ','.join(toponym["Point"]["pos"].split())
    map_params = {
        "ll": address_ll,
        "spn": ",".join(convert_pos_to_spn(toponym['boundedBy']['Envelope']['lowerCorner'],toponym['boundedBy']['Envelope']['upperCorner'])),
        "l": "map"
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    place_picture = open(f'static/img/{id}_map_picture.jpg','wb')
    place_picture.write(response.content)
    place_picture.close()
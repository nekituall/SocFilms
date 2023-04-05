import json

import requests


def search_api(name):
    TOKEN = 'TOKEN'  #вставить сюда ключ
    base_url = r'https://api.kinopoisk.dev/v1/movie?'
    param1 = name
    try:
        complete_url = base_url + "selectFields=name&selectFields=year&selectFields=genres.name&selectFields=countries.name" + '&name=' + str(param1)
        data = requests.get(complete_url, headers={'X-API-KEY': TOKEN})
        final_data = data.json()
        final_data = json.dumps(final_data, ensure_ascii=False)  #сериализует данные в удобынй вид
        final_data = json.loads(final_data)   #для записи строчки в файл нужно закомментить
        result_set = []
        for i in final_data["docs"]:
            result_set.append((i["name"], i["year"], [y["name"] for y in i["genres"]], [x["name"] for x in i["countries"]]))
        return result_set
    except:
        return None


if __name__ == "__main__":
    search_api("Титаник")
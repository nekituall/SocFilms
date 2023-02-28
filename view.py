

import requests
import json


def search_api(name):
    api_key = 'HD1BMKQ-FKM4QEE-NPR9WFW-FQGGGQ4'
    base_url = r'https://api.kinopoisk.dev/v1/movie?'
    param1 = name
    complete_url = base_url + "selectFields=name&selectFields=year&selectFields=genres.name&selectFields=countries.name" + '&name=' + str(param1)
    data = requests.get(complete_url, headers={'X-API-KEY': 'HD1BMKQ-FKM4QEE-NPR9WFW-FQGGGQ4'})
    final_data = data.json()
    final_data = json.dumps(final_data, ensure_ascii=False)  #сериализует данные в удобынй вид
    final_data = json.loads(final_data)   #для записи строчки в файл нужно закомментить
    result_set = []

    for i in final_data["docs"]:
        result_set.append((i["name"], i["year"], [y["name"] for y in i["genres"]], [x["name"] for x in i["countries"]]))
        print("Название:", i["name"], "// Год:", i["year"], "// Жанр:", [y["name"] for y in i["genres"]], "// Страна:", [x["name"] for x in i["countries"]])

    return result_set
    # return final_data["docs"]


    # записать в переменную ответ и  потом ее ковырять!!!
    # with open("api_res_fields.txt", "w") as f:
    #     data = f.write(final_data)
    #     print(type(data))
# #

# ковырять!!!
# with open("api_res_fields.txt", "r") as f:
#     data = f.read()
#     print(type(data))
#     final_data = json.loads(data)
#     print(len(final_data["docs"]))
# for i in final_data["docs"]:
#     print("Название: ", i["name"], "Год:  ", i["year"], "Страна", [x["name"] for x in i["countries"]])

if __name__ == "__main__":
    search_api("Бэтмен")


import requests
import json

api_key = 'HD1BMKQ-FKM4QEE-NPR9WFW-FQGGGQ4'

base_url = r'https://api.kinopoisk.dev/v1/movie?'

param1 = "Шерлок Холмс"



complete_url = base_url + '&name='+ param1

data = requests.get(complete_url, headers={'X-API-KEY': 'HD1BMKQ-FKM4QEE-NPR9WFW-FQGGGQ4'})
print(data)
final_data = data.json()

final_data = json.dumps(final_data, indent=4)  #сериализует данные в удобынй вид

print(final_data)


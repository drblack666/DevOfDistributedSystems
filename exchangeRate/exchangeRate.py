import json
import requests
from datetime import date
from math import trunc, floor

from zeep import Client
from zeep.helpers import serialize_object


def cbr():
    new_curs_dict = {}
    client = Client('https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL')
    service = client.bind('DailyInfo', 'DailyInfoSoap12')
    today_curs_dict = serialize_object(service.GetCursOnDate(date.today()))

    for i in range(0, len(today_curs_dict['_value_1']['_value_1'])):
        new_valute_curs = {
            today_curs_dict['_value_1']['_value_1'][i]['ValuteCursOnDate']['Vname'].strip():
                today_curs_dict['_value_1']['_value_1'][i]['ValuteCursOnDate']['Vcurs']
        }
        new_curs_dict.update(new_valute_curs)
    return new_curs_dict


def morpher(n_val, unit_val):
    url = "https://ws3.morpher.ru/russian/spell"
    params = dict(
        n=n_val,
        unit=unit_val,
        format="json",
        # token= #Не обязателен
    )
    response = requests.get(url=url, params=params)
    data = json.loads(response.text)
    return data


if __name__ == "__main__":
    valute_name = input('Enter valute name: ')
    curs_dict = cbr()
    if valute_name not in curs_dict.keys():
        print("This valute name does not exist. Choose it from the list:")
        for item in curs_dict.keys():
            print(item)
        valute_name = input('Enter valute name: ')

    valute_curs = curs_dict[valute_name]
    penny = int(round(valute_curs - floor(valute_curs), 2) * 100)

    rubles_data = morpher(trunc(valute_curs), "рубли")
    penny_data = morpher(penny, "копейки")

    print('один', valute_name.lower(), 'равен', rubles_data.get('n').get('Д'), rubles_data.get('unit').get('Д'), penny,
          penny_data.get('unit').get('Д'))

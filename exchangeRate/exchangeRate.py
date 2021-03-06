import json
import requests
from datetime import date
from math import trunc, floor

from zeep import Client
from zeep.helpers import serialize_object


def cbr(newCursDict):
    client = Client('https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL')
    service = client.bind('DailyInfo', 'DailyInfoSoap12')
    todayCursDict = serialize_object(service.GetCursOnDate(date.today()))

    for i in range(0, len(todayCursDict['_value_1']['_value_1'])):
        newValuteCurs = {
            todayCursDict['_value_1']['_value_1'][i]['ValuteCursOnDate']['Vname'].strip():
                todayCursDict['_value_1']['_value_1'][i]['ValuteCursOnDate']['Vcurs']
        }
        newCursDict.update(newValuteCurs)


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
    valuteName = input('Enter valute name: ')
    newCursDict = {}
    cbr(newCursDict)
    if valuteName not in newCursDict.keys():
        print("This valute name does not exist. Choose it from the list:")
        for item in newCursDict.keys():
            print(item)
        valuteName = input('Enter valute name: ')

    valuteCurs = newCursDict[valuteName]
    penny = int(round(valuteCurs - floor(valuteCurs), 2)*100)

    rubles_data = morpher(trunc(valuteCurs), "рубли")
    penny_data = morpher(penny, "копейки")

    print('один', valuteName.lower(), 'равен', rubles_data.get('n').get('Д'), rubles_data.get('unit').get('Д'), penny,
          penny_data.get('unit').get('Д'))

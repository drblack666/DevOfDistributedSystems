import json
import requests
from datetime import date
from math import trunc, floor

from zeep import Client
from zeep.helpers import serialize_object

valuteName = input('Enter valute name: ')

client = Client('https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL')
service = client.bind('DailyInfo', 'DailyInfoSoap12')
todayCursDict = serialize_object(service.GetCursOnDate(date.today()))

newCursDict = {}
for i in range(0, len(todayCursDict['_value_1']['_value_1'])):
    newValuteCurs = {
        todayCursDict['_value_1']['_value_1'][i]['ValuteCursOnDate']['Vname'].strip():
            todayCursDict['_value_1']['_value_1'][i]['ValuteCursOnDate']['Vcurs']
    }
    newCursDict.update(newValuteCurs)

if valuteName not in newCursDict.keys():
    print("This valuteName does not exist. Choose it from the list:")
    for item in newCursDict.keys():
        print(item)
    valuteName = input('Enter valute name: ')

valuteCurs = newCursDict[valuteName]
penny = int(round(valuteCurs - floor(valuteCurs), 2)*100)

url = "https://ws3.morpher.ru/russian/spell"
params = dict(
    n=trunc(valuteCurs),
    unit="рубли",
    format="json",
    #token= #Не обязателен. Подробнее: http://morpher.ru/ws3/#authentication
)

response = requests.get(url=url, params=params)
data = json.loads(response.text)

params02 = dict(
    n=penny,
    unit="копейки",
    format="json",
    #token= #Не обязателен. Подробнее: http://morpher.ru/ws3/#authentication
)

response02 = requests.get(url=url, params=params02)
data02 = json.loads(response02.text)
print('один', valuteName.lower(), 'равен', data.get('n').get('Д'), data.get('unit').get('Д'), penny,
      data02.get('unit').get('Д'))

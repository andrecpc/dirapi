#   d:
#   cd C:\Python27
#   python dirapi5.py
#   OverdraftSumAvailable  / 1000000

import requests, json, urllib2
from requests.exceptions import ConnectionError
from time import sleep
import sys

if sys.version_info < (3,):
    def u(x):
        try:
            return x.encode("utf8")
        except UnicodeDecodeError:
            return x
else:
    def u(x):
        if type(x) == type(b''):
            return x.decode('utf8')
        else:
            return x
def getclients():
    #URL = 'https://api-sandbox.direct.yandex.com/json/v5/agencyclients'
    URL = 'https://api.direct.yandex.com/json/v5/agencyclients'

    token = 'AQAxxxxxxxxxxxxxn3THGzf0'

    headers = {"Authorization": "Bearer " + token,"Accept-Language": "ru"}

    body = {"method": "get", "params": {"SelectionCriteria": {"Archived": "NO"}, "FieldNames": ["Login", "OverdraftSumAvailable"]}}

    jsonBody = json.dumps(body, ensure_ascii=False).encode('utf8')

    info_clients = []
    logins = []
    balans = []

    try:
        result = requests.post(URL, jsonBody, headers=headers)

        if result.status_code != 200 or result.json().get("error", False):
            print("proizoshla oshibka.")
            print("kod oshibki: {}".format(result.json()["error"]["error_code"]))
            print("opisanie oshibki: {}".format(u(result.json()["error"]["error_detail"])))
            print("RequestId saprosa: {}".format(result.headers.get("RequestId", False)))
        else:
            print("RequestId saprosa: {}".format(result.headers.get("RequestId", False)))
            print("infa o ballah: {}".format(result.headers.get("Units", False)))

            for client in result.json()["result"]["Clients"]:
                logins.append(client['Login'])
                balans.append(client['OverdraftSumAvailable'])
                print("Klient: {} s balansom {}".format(u(client['Login']), client['OverdraftSumAvailable']))

            if result.json()['result'].get('LimitedBy', False):

                print("polucheni ne vse objekti.")


    except ConnectionError:

        print("oshibka soedineniya s serverom.")


    except:

        print("oshibka.")
    info_clients.append(logins)
   # info_clients.append(balans)
    print (info_clients)
    return info_clients


def get_balans():

    clients = getclients()
    ostatki = []
    logins = []
    info_clients = []
    #url = 'https://api-sandbox.direct.yandex.ru/live/v4/json/'
    url = 'https://api.direct.yandex.ru/live/v4/json/'


    token = 'AQAAAAAxxxxxxxxxxxxxCdn3THGzf0'


    for login in clients[0]:

        try:

            data = {
                'method': 'AccountManagement',
                'token': token,
                'locale': 'ru',
                'param': {
                'Action': 'Get',
                'SelectionCriteria': {
                'Logins': [login]
                }
            }
            }



            jdata = json.dumps(data, ensure_ascii=False).encode('utf8')


            response = urllib2.urlopen(url, jdata)

            amount = response.read().decode('utf8')

            dannie = json.loads(amount)

            print dannie['data']['Accounts'][0]['Amount']
            ostatki.append(dannie['data']['Accounts'][0]['Amount'])
            logins.append(login)

        except (IndexError):
            print (login + ' not found')

    info_clients.append(logins)
    info_clients.append(ostatki)
    print info_clients
    return info_clients

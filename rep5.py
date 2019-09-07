#   d:
#   cd C:\Python27
#   python dirapi5.py
#   OverdraftSumAvailable  / 1000000
#   python rep5.py

import requests, json
from requests.exceptions import ConnectionError
from time import sleep
import sys

from dirapi5 import get_balans

logins = get_balans()
#logins = [[u'koffee', u'ArkRK', u'GruzRK', u'UsedCarsRK'], [u'0', u'60942.05', u'21.84', u'41375.12']]

costs = []

def report():
    # URL = 'https://api-sandbox.direct.yandex.com/json/v5/reports'
    URL = 'https://api.direct.yandex.com/json/v5/reports'

    token = 'AQAAAAATg9xxxxxxxxxxn3THGzf0'
    for clientLogin in logins[0]:
        cost = 0

        headers = {"Authorization": "Bearer " + token,
        "Accept-Language": "ru",
        "Client-Login": clientLogin,
        "processingMode":"auto",
        "returnMoneyInMicros": "false"}

        body = {
      "params" : {
        "SelectionCriteria": {
        },
        "FieldNames": [( "Cost" )],
        "ReportName": ('rashodi'),
        "ReportType": ( "ACCOUNT_PERFORMANCE_REPORT"),
        "DateRangeType": ( "LAST_7_DAYS" ),
        "Format": ( "TSV" ),
        "IncludeVAT": ( "NO" ),
        "IncludeDiscount": ( "NO" )
      }
    }

        jsonBody = json.dumps(body, ensure_ascii=False).encode('utf8')
        while True:


            try:
                req = requests.post(URL, jsonBody, headers=headers)

                req.encoding = 'utf-8'
                if req.status_code == 400:
                    break
                elif req.status_code == 200:
                    if req.text != "":
                        cost = req.text.split("\n")[2]

                        if cost == 'Total rows: 0':
                            cost = 0
                        #print cost
                    else:
                        cost = 0
                    break
                elif req.status_code == 201:
                    retryIn = int(req.headers.get("retryIn", 60))
                    sleep(retryIn)
                elif req.status_code == 202:
                    retryIn = int(req.headers.get("retryIn", 60))
                    sleep(retryIn)
                elif req.status_code == 500:
                    break
                elif req.status_code == 502:
                    break
                else:
                    break

            except ConnectionError:
                break
            except:
                break
        #print cost
        costs.append(cost)


    print (costs)
    logins.append(costs)
    print (logins)
    return logins


#report()
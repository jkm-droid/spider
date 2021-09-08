import json
import urllib
from urllib.request import urlopen

import requests

url = "http://movieapi.mblog.co.ke/getdata.php"


def getresponse(url):
    operUrl = urllib.request.urlopen(url)
    if operUrl.getcode() == 200:
        data = operUrl.read()
        #json_data = json.loads(data)

        print(data)
    else:
        print("Error receiving data", operUrl.getcode())


if __name__ == '__main__':
    getresponse(url)
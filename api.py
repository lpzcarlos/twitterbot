
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
parameters = {
  'symbol':'GARD',

}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '00df95b4-07b9-4fe5-bed8-304fc7ce9c47',
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
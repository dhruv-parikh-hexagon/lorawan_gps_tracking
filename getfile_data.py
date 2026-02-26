import requests

url = 'http://192.168.1.137:5000'
response = requests.get(url)
abc = response.status_code

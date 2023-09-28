import requests

data = requests.get("http://127.0.0.1:8000/api/rates/?from=USD&to=GBP&value=1000")
print(data.text)
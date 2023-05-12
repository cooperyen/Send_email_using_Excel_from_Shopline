import requests

url = "https://api.millionverifier.com/api/v3/?api=Ob3F6xDemZzkFV4QVppLjzOvs&email=cooper.rafagodfsdfs@gmdail.com&timeout=10"

response = requests.request("GET", url)

print(response.text)

import requests

url = "http://192.168.100.244:8001/api/facturas/?pedido=40"
response = requests.get(url)
print("Status Code:", response.status_code)
if response.status_code == 500:
    print(response.text)

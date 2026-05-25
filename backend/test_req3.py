import requests

url = "http://192.168.100.244:8001/api/clientes/login/"
resp = requests.post(url, json={"correo": "qqqq@gmail.com", "password": "qqqq"})
token = resp.json().get('access')

url2 = "http://192.168.100.244:8001/api/facturas/?pedido=40"
resp2 = requests.get(url2, headers={"Authorization": f"Bearer {token}"})
print("Status Code:", resp2.status_code)
print(resp2.text)

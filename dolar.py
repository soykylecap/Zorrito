import requests

class DolarBlue:
    def compra():
        response = requests.get("https://dolarapi.com/v1/ambito/dolares/blue")
        datos = response.json()
        compra = datos.get('compra', 1)
        return compra
    
    def venta():
        response = requests.get("https://dolarapi.com/v1/ambito/dolares/blue")
        datos = response.json()
        venta = datos.get('venta', 1)
        return venta

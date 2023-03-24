from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
# from bs4 import BeautifulSoup
import json



ruta = ChromeDriverManager(path='./chromedriver').install()
print(ruta)

s = Service(ruta)
driver = webdriver.Chrome(service=s)
url = "http://gis.sutran.gob.pe/alerta_sutran/"

texto_response =""


driver.get(url)
for request in driver.requests:
    if request.response:
        if request.method == 'POST' and request.url.split('/')[-1] == 'carga_xlsx.php':
            print(
                request.url,
                request.response.status_code,
                request.response.headers['Content-Type'],
                
            )
            texto_response = request.response.body.decode('utf-8-sig')

#####Exportando data completa

json_response = json.loads(texto_response) #paratrabajar en python
json_response_write = json.dumps(json_response, indent=4) # metodo que exporta nuestra data a json
with open('data.json',"w") as f:
    f.write(json_response_write)

#####Exportando data filtrada

filtrado = []


for c,v in json_response.items():
    if c == 'restringido' or c == 'interrumpido':
        for data_item in json_response[c]:
            if data_item["properties"]["motivo"] == "HUMANO":
                filtrado.append(data_item)
                
#Guardamos un nuevo json para nuestrada datafiltrada
json_export = json.dumps(filtrado, indent=4)
with open('datafiltradafinalizada.json', 'w') as file:
    file.write(json_export)


#para que selenium no se cierre
input("Enter para acabar")
 





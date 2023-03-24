from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
# from bs4 import BeautifulSoup
import json


#instalamos nuestro chrome drive manager
ruta = ChromeDriverManager(path='./chromedriver').install()
#creamos el servicio en base a cromhe
s = Service(ruta)
#instanciamos una instancia del webdriver chrome en base al servicio anterior con seleniumwire
driver = webdriver.Chrome(service=s)
#features
url = "http://gis.sutran.gob.pe/alerta_sutran/"
nombre_buscar = 'carga_xlsx.php'



def obtener_POST(url,name_file):
    driver.get(url)
    for request in driver.requests:
        if request.response:
            if request.method == 'POST' and request.url.split('/')[-1] == name_file:
                print(
                    request.url,
                    request.response.status_code,
                    request.response.headers['Content-Type'],
                    
                )
                texto_response = request.response.body.decode('utf-8-sig')
    return texto_response



#####Exportando data completa
texto_respuesta = obtener_POST(url, nombre_buscar)
json_response = json.loads(texto_respuesta) #paratrabajar en python
json_response_write = json.dumps(json_response, indent=4) # metodo que exporta nuestra data a json
with open('data.json',"w") as f:
    f.write(json_response_write)

#####Exportando data filtrada según lo solicitado

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
 





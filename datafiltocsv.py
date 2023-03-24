import json
import csv

with open("datafiltradafinalizada.json", "r") as f:
    jsonDatos = json.load(f)

data_file = open("data_details.csv", "w", encoding="utf-8")
csv_writer = csv.writer(data_file, lineterminator='\n')
contador = 0
for data in jsonDatos:
    if contador == 0:
        #para las cabeceras
        header = data["properties"].keys()
        csv_writer.writerow(header)
        contador+=1
    #para cada fila
    csv_writer.writerow(data["properties"].values())
    
data_file.close()
    

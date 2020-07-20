import urllib.request as request, json, numpy as np

with request.urlopen("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province-latest.json") as response:
    source = response.read()
    data = json.loads(source)

num_province = len(data)
num_regioni = 20
names_regioni = []
tot_regioni = np.zeros(num_regioni, dtype = int)
list_regioni = []

for i in range(1, num_regioni+1):
    for j in range(num_province):
        if data[j]["codice_regione"] == i:
            name = data[j]["denominazione_regione"]
            if "P.A." in name:
                name = "Trentino - Alto Adige"
            names_regioni.append(name)
            break

for j in range(num_province):
    i = data[j]["codice_regione"] - 1
    tot_provincia = data[j]["totale_casi"]
    tot_regioni[i] += tot_provincia

for i in range(num_regioni):
    list_regioni += ((names_regioni[i], tot_regioni[i]), )
list_regioni.sort(key = lambda x: (-x[1], x[0]))

print("---Numero totale di casi per regione in ordine decrescente---")
for i in range(num_regioni):
    print("%25s %d" %(list_regioni[i][0] + ": ", list_regioni[i][1]))
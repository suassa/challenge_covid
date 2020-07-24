import urllib.request, json, numpy


with urllib.request.urlopen("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province-latest.json") as response:
    source = response.read()
    data = json.loads(source)


num_regioni = 20


names_regioni = []

for i in range(1, num_regioni + 1):
    if i == 4:
        names_regioni.append("Trentino - Alto Adige")
    else:
        for j, obj in enumerate(data):
            if obj["codice_regione"] == i:
                name = obj["denominazione_regione"]
                names_regioni.append(name)
                break


tot_regioni = numpy.zeros(num_regioni, dtype = int)

for obj in data:
    i = obj["codice_regione"] - 1
    if i > 19:  # Eccezione per Trentino diviso nelle due P.A. (cod 4 Trentino, cod 21 e 22 per le due P.A.).
        i = 3
    tot_regioni[i] += obj["totale_casi"]


list_regioni = []

for i, name in enumerate(names_regioni):
    list_regioni += [[name, tot_regioni[i]], ]
list_regioni.sort(key=lambda x: (-x[1], x[0]))


print("---Numero totale di casi per regione, in ordine decrescente---")
for row in list_regioni:
    print("%23s %d" % (row[0] + ": ", row[1]))
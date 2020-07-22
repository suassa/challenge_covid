from flask import Flask, render_template, request
from datetime import datetime
import urllib
import json
import numpy



def find_date(json_obj, date):
    return[obj for obj in json_obj if str(date) in obj["data"]]


def get_names(data, nr, np):
    list= []
    for i in range(1, nr + 1):
        if i ==4:
            list.append("Trentino - Alto Adige")
        else:
            for j in range(np):
                if data[j]["codice_regione"] == i:
                    name = data[j]["denominazione_regione"]
                    list.append(name)
                    break
    return(list)


def calc_total(data, nr, np):
    tot_regioni = numpy.zeros(nr, dtype = int)
    for j in range(np):
        i = data[j]["codice_regione"] - 1
        if i > 19: #Eccezione per Trentino diviso nelle due P.A. (cod 4 Trentino, cod 21 e 22 per le due P.A.).
            i = 3
        tot_provincia = data[j]["totale_casi"]
        tot_regioni[i] += tot_provincia
    return(tot_regioni)


def sort_list(names, tot):
    list = []
    for i in range(len(names)):
        list += ((names[i], tot[i]), )
    list.sort(key = lambda x: (-x[1], x[0]))
    return list


def search_and_sort(date_requested):

    with urllib.request.urlopen("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province.json") as response:
        source = response.read()
        all_data = json.loads(source)

    data = find_date(all_data, date_requested)

    num_province = len(data)
    num_regioni = 20

    names_regioni = get_names(data, num_regioni, num_province)
    tot_regioni = calc_total(data, num_regioni, num_province)
    list_regioni = sort_list(names_regioni, tot_regioni)

    return list_regioni[1][0]



app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ricerca")
def search():
    date = request.args.get("date")
    date = datetime.strptime(date, "%Y-%m-%d").date()
    table = search_and_sort(date)
    return table

if __name__ == "__main__":
    app.run(debug = True)
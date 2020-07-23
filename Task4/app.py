from flask import Flask, render_template, request, Markup
from datetime import datetime
from mako.template import Template
import urllib
import json
import numpy
import xlwt

class DataStore():
    date = None
    results = None
    num_regioni = 20

datastore = DataStore()


def find_date(json_obj, date):
    return[obj for obj in json_obj if str(date) in obj["data"]]


def get_names(data, np):
    list= []
    nr = datastore.num_regioni
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


def calc_total(data, np):
    nr = datastore.num_regioni
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
    nr= datastore.num_regioni
    for i in range(nr):
        list += ((names[i], tot[i]), )
    list.sort(key = lambda x: (-x[1], x[0]))
    return list


def search_and_sort():
    date_requested = datastore.date

    with urllib.request.urlopen("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province.json") as response:
        source = response.read()
        all_data = json.loads(source)

    data = find_date(all_data, date_requested)

    num_province = len(data)

    names_regioni = get_names(data, num_province)
    tot_regioni = calc_total(data, num_province)
    list_regioni = sort_list(names_regioni, tot_regioni)
    datastore.results = list_regioni

    template = """
            <table>
                <tr>
                    <th> 
                        Regione 
                    </th>
                    
                    <th>
                        Totale casi
                    </th>
                %for row in rows:
                    <tr>
                        %for cell in row:
                            <td>${cell}</td>
                        %endfor
                    </tr>
                %endfor
            </table>
                """

    table = Template(template).render(rows=list_regioni)

    return table


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ricerca")
def search():
    date = request.args.get("date")
    date = datetime.strptime(date, "%Y-%m-%d").date()
    datastore.date = date
    date = str(date.day)+"/"+str(date.month)+"/"+str(date.year)
    result = Markup(search_and_sort())
    return render_template("result.html", date = date, result = result)

@app.route("/save")
def save():
    date = datastore.date
    nr = datastore.num_regioni
    list = datastore.results

    wb = xlwt.Workbook()
    date_new_format = str(date.day)+"-"+str(date.month)+"-"+str(date.year)
    sheet = wb.add_sheet(date_new_format)

    title_style = xlwt.easyxf("font: bold 1, height 280, color red")
    label_style = xlwt.easyxf("font: bold 1, height 240, color red")
    text_style = xlwt.easyxf("font: height 240, color black")

    sheet.write(0, 0, "Numero totale di casi per regione al giorno "+ date_new_format + ", in ordine decrescente", title_style)
    sheet.write(2, 0, "Regione", label_style)
    sheet.write(2, 1, "Totale casi al giorno " + date_new_format, label_style)

    row = 3
    for i in range(nr):
        sheet.write(row, 0, list[i][0], text_style)
        sheet.write(row, 1, str(list[i][1]), text_style)
        row +=1
    wb.save(date_new_format + ".xls")
    return "File salvato"

if __name__ == "__main__":
    app.run(debug = True)
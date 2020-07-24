import datetime
import json
import numpy
import urllib.request
import xlwt


def get_input():
    date_input = input("Inserisci una data compresa tra il 24/02/2020 e la data corrente nel formato GG/MM/AAAA")
    if not date_input.replace("/", "").isdigit() or len(date_input) != 10:
        print("Formato non riconosciuto")
        get_input()

    day = int(date_input[:2])
    month = int(date_input[3:5])
    year = int(date_input[6:])
    date_requested = datetime.date(year, month, day)
    min_date = datetime.date(2020, 2, 24)

    if date_requested < min_date or date_requested > datetime.date.today():
        print("La data inserita non è valida")
        get_input()
    return(date_requested)


def find_date(json_obj, date):
    return[obj for obj in json_obj if str(date) in obj["data"]]


def get_names(data, nr):
    names= []
    for i in range(1, nr + 1):
        if i ==4:
            names.append("Trentino - Alto Adige")
        else:
            for j, obj in enumerate(data):
                if obj["codice_regione"] == i:
                    name = obj["denominazione_regione"]
                    names.append(name)
                    break
    return(names)


def calc_total(data, nr):
    tot_regioni = numpy.zeros(nr, dtype = int)
    for obj in data:
        i = obj["codice_regione"] - 1
        if i > 19: #Eccezione per Trentino diviso nelle due P.A. (cod 4 Trentino, cod 21 e 22 per le due P.A.).
            i = 3
        tot_regioni[i] += obj["totale_casi"]
    return(tot_regioni)


def sort_list(names, tot):
    sorted_list = []
    for i, name in enumerate(names):
        sorted_list += [[name, tot[i]], ]
    sorted_list.sort(key = lambda x: (-x[1], x[0]))
    return sorted_list


def save_input():
    reply = input("Vuoi salvare i dati? (Sì/no)").lower()
    if reply[0] == "n":
        quit()
    elif reply[0] != "s":
        print("La risposta inserita non è valida.")
        save_input()


def save_xls(date, num, list):
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
    for e in list:
        sheet.write(row, 0, e[0], text_style)
        sheet.write(row, 1, str(e[1]), text_style)
        row +=1

    wb.save(date_new_format+".xls")


def main():
    date_requested = get_input()

    with urllib.request.urlopen("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province.json") as response:
        source = response.read()
        all_data = json.loads(source)

    data = find_date(all_data, date_requested)

    num_regioni = 20

    names_regioni = get_names(data, num_regioni)
    tot_regioni = calc_total(data, num_regioni)
    list_regioni = sort_list(names_regioni, tot_regioni)

    print("---Numero totale di casi per regione, in ordine decrescente---")
    for row in list_regioni:
        print("%23s %d" % (row[0] + ": ", row[1]))

    save_input()
    save_xls(date_requested, num_regioni, list_regioni)


if __name__ == "__main__":
    main()
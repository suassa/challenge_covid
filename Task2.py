import urllib.request as request, json, numpy as np, datetime

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

def get_names(data, num_regioni, num_province):
    list= []
    for i in range(1, num_regioni + 1):
        if i ==4:
            list.append("Trentino - Alto Adige")
        for j in range(num_province):
            if data[j]["codice_regione"] == i:
                name = data[j]["denominazione_regione"]
                list.append(name)
                break
    return(list)

def calc_total(data, num_regioni, num_province):
    tot_regioni = np.zeros(num_regioni, dtype = int)
    for j in range(num_province):
        i = data[j]["codice_regione"] - 1
        if i > 19: #Eccezione per Trentino diviso nelle due P.A. (cod 4 Trentino, cod 21 e 22 per le due P.A.).
            i = 3
        tot_provincia = data[j]["totale_casi"]
        tot_regioni[i] += tot_provincia
    return(tot_regioni)

def sort_list(names, tot, num):
    list = []
    for i in range(num):
        list += ((names[i], tot[i]), )
    list.sort(key = lambda x: (-x[1], x[0]))
    return list

def main():
    date_requested = get_input()

    with request.urlopen("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province.json") as response:
        source = response.read()
        all_data = json.loads(source)

    data = find_date(all_data, date_requested)

    num_province = len(data)
    num_regioni = 20

    names_regioni = get_names(data, num_regioni, num_province)
    tot_regioni = calc_total(data, num_regioni, num_province)
    list_regioni = sort_list(names_regioni, tot_regioni, num_regioni)

    print("---Numero totale di casi per regione, in ordine decrescente---")
    for i in range(num_regioni):
        print("%23s %d" % (list_regioni[i][0] + ": ", list_regioni[i][1]))

if __name__ == "__main__":
    main()
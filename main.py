from tkinter import *

import tkintermapview

teatry: list = []
clients: list = []
workers: list = []


class Teatr:
    def __init__(self, teatry_name, teatry_location):
        self.teatry_name = teatry_name
        self.location = teatry_location
        self.coordinates = self.get_coordinates()
        if self.coordinates:
            self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1],
                                                text=f'Teatry: {self.teatry_name}')
        else:
            self.marker = None

    def get_coordinates(self):
        import requests
        from bs4 import BeautifulSoup
        try:
            url = f"https://pl.wikipedia.org/wiki/{self.location}"
            response = requests.get(url).text
            soup = BeautifulSoup(response, "html.parser")
            lon_elements = soup.select(".longitude")
            lat_elements = soup.select(".latitude")
            if not lon_elements or not lat_elements:
                raise ValueError("Brak współrzędnych w artykule.")
            lon = float(lon_elements[1].text.replace(",", ".")) if len(lon_elements) > 1 else float(
                lon_elements[0].text.replace(",", "."))
            lat = float(lat_elements[1].text.replace(",", ".")) if len(lat_elements) > 1 else float(
                lat_elements[0].text.replace(",", "."))
            return [lat, lon]
        except Exception as e:
            print(f"Błąd przy pobieraniu współrzędnych dla {self.location}: {e}")
            return None

class Client:
    def __init__(self, name, location, theater):
        self.name = name
        self.location = location
        self.theater = theater
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f'Klient: {self.name}')
        if self.coordinates:
            self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f'Klient: {self.name}')
        else:
            self.marker = None

    def get_coordinates(self):
        import requests
        from bs4 import BeautifulSoup
        url = f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        lon = float(soup.select(".longitude")[1].text.replace(",", "."))
        lat = float(soup.select(".latitude")[1].text.replace(",", "."))
        return [lat, lon]


class Worker:
    def __init__(self, name, location, theater):
        self.name = name
        self.location = location
        self.theater = theater
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f'Pracownik: {self.name}')
        if self.coordinates:
            self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f'Pracownik: {self.name}')
        else:
            self.marker = None

    def get_coordinates(self):
        import requests
        from bs4 import BeautifulSoup
        url = f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        lon = float(soup.select(".longitude")[1].text.replace(",", "."))
        lat = float(soup.select(".latitude")[1].text.replace(",", "."))
        return [lat, lon]


def add_teatry():
    zmienna_nazwa = entry_teatry_name.get()
    zmienna_miejscowosc = entry_location.get()
    nowy_teatr = Teatr(zmienna_nazwa, zmienna_miejscowosc)
    teatry.append(nowy_teatr)
    entry_teatry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_teatry_name.focus()
    show_teatry()




def show_teatry():
    listbox_lista_obiketow.delete(0, END)
    for idx, teatr in enumerate(teatry):
        listbox_lista_obiketow.insert(idx, f'{idx + 1}. {teatr.teatry_name}')


def remove_teatry():
    i = listbox_lista_obiketow.index(ACTIVE)
    teatry[i].marker.delete()
    teatry.pop(i)
    show_teatry()


def edit_teatry():
    i = listbox_lista_obiketow.index(ACTIVE)
    teatry_name = teatry[i].teatry_name

    location = teatry[i].location

    entry_teatry_name.insert(0, teatry_name)
    entry_location.insert(0, location)

    button_dodaj_obiekt.config(text='zapisz', command=lambda: update_teatry(i))


def update_teatry(i):
    new_teatry_name = entry_teatry_name.get()
    new_location = entry_location.get()


    teatry[i].teatry_name = new_teatry_name

    teatry[i].location = new_location


    teatry[i].marker.delete()
    teatry[i].coordinates = teatry[i].get_coordinates()
    if teatry[i].coordinates:
        teatry[i].marker = map_widget.set_marker(teatry[i].coordinates[0], teatry[i].coordinates[1])
    else:
        teatry[i].marker = None

    entry_teatry_name.delete(0, END)
    entry_location.delete(0, END)

    entry_teatry_name.focus()

    button_dodaj_obiekt.config(text='Dodaj obiekt', command=add_teatry)
    show_teatry()


def show_teatry_details():
    i = listbox_lista_obiketow.index(ACTIVE)
    teatry_name = teatry[i].teatry_name
    location = teatry[i].location
    label_szczegoly_teatry_name_wartosc.config(text=teatry_name)
    label_szczegoly_location_wartosc.config(text=location)

    map_widget.set_position(teatry[i].coordinates[0], teatry[i].coordinates[1])
    map_widget.set_zoom(17)

def add_client():
    name = entry_klient_name.get()
    location = entry_klient_location.get()
    index = int(entry_klient_teatr.get()) - 1
    listbox_pracownikow.insert(END, f'{name} ({location})')
    if 0 <= index < len(teatry):
        klient = Client(name, location, teatry[index])
        clients.append(klient)
        entry_klient_name.delete(0, END)
        entry_klient_location.delete(0, END)
        entry_klient_teatr.delete(0, END)


def add_worker():
    name = entry_pracownik_name.get()
    location = entry_pracownik_location.get()
    index = int(entry_pracownik_teatr.get()) - 1
    listbox_pracownikow.insert(END, f'{name} ({location})')

    if 0 <= index < len(teatry):
        pracownik = Worker(name, location, teatry[index])
        workers.append(pracownik)
        entry_pracownik_name.delete(0, END)
        entry_pracownik_location.delete(0, END)
        entry_pracownik_teatr.delete(0, END)

def remove_client():
    i = listbox_klientow.curselection()
    if i:
        index = i[0]
        clients[index].marker.delete()
        clients.pop(index)
        listbox_klientow.delete(index)

def remove_worker():
    i = listbox_pracownikow.curselection()
    if i:
        index = i[0]
        workers[index].marker.delete()
        workers.pop(index)
        listbox_pracownikow.delete(index)

root = Tk()
root.geometry("1200x760")
root.title("Projekt MG")

ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly_obiektow = Frame(root)
ramka_mapa = Frame(root)

ramka_lista_obiektow.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_obiektow.grid(row=1, column=0, columnspan=2)
ramka_mapa.grid(row=2, column=0, columnspan=2)

# Lista klientów
label_lista_klientow = Label(ramka_lista_obiektow, text="Lista klientów")
label_lista_klientow.grid(row=3, column=1, columnspan=3)
listbox_klientow = Listbox(ramka_lista_obiektow, width=50, height=5)
listbox_klientow.grid(row=4, column=1, columnspan=3)
button_usun_klienta = Button(ramka_lista_obiektow, text="Usuń klienta", command=lambda: remove_client())
button_usun_klienta.grid(row=5, column=1)

# Lista pracowników
label_lista_pracownikow = Label(ramka_lista_obiektow, text="Lista pracowników")
label_lista_pracownikow.grid(row=6, column=0, columnspan=3)
listbox_pracownikow = Listbox(ramka_lista_obiektow, width=50, height=5)
listbox_pracownikow.grid(row=7, column=0, columnspan=3)
button_usun_pracownika = Button(ramka_lista_obiektow, text="Usuń pracownika", command=lambda: remove_worker())
button_usun_pracownika.grid(row=8, column=0)

# === Formularz klientów ===
label_klienci = Label(ramka_formularz, text="Dodaj klienta")
label_klienci.grid(row=6, column=0, columnspan=2)

label_klient_name = Label(ramka_formularz, text="Imię klienta:")
label_klient_name.grid(row=7, column=0)
entry_klient_name = Entry(ramka_formularz)
entry_klient_name.grid(row=7, column=1)

label_klient_location = Label(ramka_formularz, text="Miejscowość:")
label_klient_location.grid(row=8, column=0)
entry_klient_location = Entry(ramka_formularz)
entry_klient_location.grid(row=8, column=1)

label_klient_teatr = Label(ramka_formularz, text="Nr teatru:")
label_klient_teatr.grid(row=9, column=0)
entry_klient_teatr = Entry(ramka_formularz)
entry_klient_teatr.grid(row=9, column=1)

button_dodaj_klienta = Button(ramka_formularz, text="Dodaj klienta", command=lambda: add_client())
button_dodaj_klienta.grid(row=10, column=0, columnspan=2)


# === Formularz pracowników ===
label_pracownicy = Label(ramka_formularz, text="Dodaj pracownika")
label_pracownicy.grid(row=11, column=0, columnspan=2)

label_pracownik_name = Label(ramka_formularz, text="Imię pracownika:")
label_pracownik_name.grid(row=12, column=0)
entry_pracownik_name = Entry(ramka_formularz)
entry_pracownik_name.grid(row=12, column=1)

label_pracownik_location = Label(ramka_formularz, text="Miejscowość:")
label_pracownik_location.grid(row=13, column=0)
entry_pracownik_location = Entry(ramka_formularz)
entry_pracownik_location.grid(row=13, column=1)

label_pracownik_teatr = Label(ramka_formularz, text="Nr teatru:")
label_pracownik_teatr.grid(row=14, column=0)
entry_pracownik_teatr = Entry(ramka_formularz)
entry_pracownik_teatr.grid(row=14, column=1)

button_dodaj_pracownika = Button(ramka_formularz, text="Dodaj pracownika", command=lambda: add_worker())
button_dodaj_pracownika.grid(row=15, column=0, columnspan=2)

# ramka_lista_obiektow
label_lista_obiektow = Label(ramka_lista_obiektow, text="Lista użytkowników")
label_lista_obiektow.grid(row=0, column=0, columnspan=3)
listbox_lista_obiketow = Listbox(ramka_lista_obiektow, width=50, height=10)
listbox_lista_obiketow.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly_obiektu = Button(ramka_lista_obiektow, text='Pokaż szczegóły', command=show_teatry_details)
button_pokaz_szczegoly_obiektu.grid(row=2, column=0)
button_usun_obiekt = Button(ramka_lista_obiektow, text='Usuń obiekt', command=remove_teatry)
button_usun_obiekt.grid(row=2, column=1)
button_edytuj_obiekt = Button(ramka_lista_obiektow, text='Edytuj obiekt', command=edit_teatry)
button_edytuj_obiekt.grid(row=2, column=2)

# ramka_formularz
label_formularz = Label(ramka_formularz, text="Formularz")
label_formularz.grid(row=0, column=0, columnspan=2)
label_teatry_name = Label(ramka_formularz, text="Nazwa Teatru:")
label_teatry_name.grid(row=1, column=0, sticky=W)
label_location = Label(ramka_formularz, text="Miejscowość:")
label_location.grid(row=2, column=0, sticky=W)


entry_teatry_name = Entry(ramka_formularz)
entry_teatry_name.grid(row=1, column=1)
entry_location = Entry(ramka_formularz)
entry_location.grid(row=2, column=1)

button_dodaj_obiekt = Button(ramka_formularz, text='Dodaj obiekt', command=add_teatry)
button_dodaj_obiekt.grid(row=5, column=0, columnspan=2)

# ramka_szczegoly_obiektow
label_szczegoly_obiektow = Label(ramka_szczegoly_obiektow, text="Szczegoly obiektu:")
label_szczegoly_obiektow.grid(row=0, column=0)
label_szczegoly_teatry_name = Label(ramka_szczegoly_obiektow, text="Nazwa Teatru:")
label_szczegoly_teatry_name.grid(row=1, column=0)
label_szczegoly_teatry_name_wartosc = Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_teatry_name_wartosc.grid(row=1, column=1)
label_szczegoly_location = Label(ramka_szczegoly_obiektow, text="Miejscowość:")
label_szczegoly_location.grid(row=1, column=4)
label_szczegoly_location_wartosc = Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_location_wartosc.grid(row=1, column=5)
label_szczegoly__wartosc = Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly__wartosc.grid(row=1, column=7)

# ramka_mapa
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=500, corner_radius=5)
map_widget.grid(row=0, column=0, columnspan=2)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)

root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import tkintermapview
import requests
from bs4 import BeautifulSoup

teatry = []
clients = []
workers = []

class Teatr:
    def __init__(self, teatry_name, teatry_location, map_widget):
        self.teatry_name = teatry_name
        self.location = teatry_location
        self.coordinates = self.get_coordinates()
        self.marker = None
        if self.coordinates:
            self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1],
                                                text=f'Teatry: {self.teatry_name}')
        else:
            self.marker = None

    def get_coordinates(self):
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
    def __init__(self, name, location, theater, map_widget):
        self.name = name
        self.location = location
        self.theater = theater
        self.coordinates = self.get_coordinates()
        self.marker = None
        if self.coordinates:
            self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f'Klient: {self.name}')
        else:
            self.marker = None

    def get_coordinates(self):
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
            print(f"Błąd przy pobieraniu współrzędnych dla klienta {self.location}: {e}")
            return None

class Worker:
    def __init__(self, name, location, theater, specialization, map_widget):
        self.name = name
        self.location = location
        self.specialization = specialization
        self.theater = theater
        self.coordinates = self.get_coordinates()
        self.marker = None
        if self.coordinates:
            text = f'Pracownik: {self.name}\nSpecjalizacja: {self.specialization}'
            self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=text)
        else:
            self.marker = None

    def get_coordinates(self):
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
            print(f"Błąd przy pobieraniu współrzędnych dla pracownika {self.location}: {e}")
            return None

clients_visible = True
workers_visible = True
theaters_visible = True

def add_teatr(name, location):
    name = theater_name_entry.get()
    location = theater_address_entry.get()
    teatry = Teatr(name, location, map_widget)#-#

    if not name or not location:
        messagebox.showwarning("Brak danych", "Wprowadź nazwę i location teatru.")
        return

    teatr = Teatr(name, location)
    if teatr.coordinates is None:
        messagebox.showerror("Błąd", f"Nie udało się znaleźć współrzędnych dla locationu: {location}")
        return

    teatry.append(teatr)
    listbox_theater.insert(tk.END, f'{name} ({location})')
    theater_name_entry.delete(0, tk.END)
    theater_address_entry.delete(0, tk.END)
    messagebox.showinfo("Sukces", f"Dodano teatr: {name}")


def add_client(name, location, theater_name):
    name = client_name_entry.get()
    location = client_location_entry.get()
    try:
        index = int(client_theater_entry.get()) - 1
    except ValueError:
        messagebox.showwarning("Błąd", "Podaj prawidłowy numer teatru.")
        return

    if not name or not location:
        messagebox.showwarning("Brak danych", "Wprowadź imię i lokalizację klienta.")
        return

    if 0 <= index < len(teatry):
        klient = Client(name, location, map_widget)
        if klient.coordinates is None:
            messagebox.showerror("Błąd", f"Nie udało się pobrać współrzędnych dla klienta {location}.")
            return
        clients.append(klient)
        listbox_klientow.insert(tk.END, f'{name} ({location})')
        client_name_entry.delete(0, tk.END)
        client_location_entry.delete(0, tk.END)
        client_theater_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Błąd", "Podaj prawidłowy numer teatru.")

def add_worker(name, location, specialization, theater_name):
    name = staff_name_entry.get()
    location = staff_location_entry.get()
    specialization = staff_specialization_entry.get()
    if not specialization:
        messagebox.showwarning("Brak danych", "Wybierz specjalizację pracownika.")
        return
    try:
        index = int(staff_theater_entry.get()) - 1
    except ValueError:
        messagebox.showwarning("Błąd", "Podaj prawidłowy numer teatru.")
        return

    if not name or not location:
        messagebox.showwarning("Brak danych", "Wprowadź imię i lokalizację pracownika.")
        return

    if 0 <= index < len(teatry):
        pracownik = Worker(name, location, teatry, specialization, map_widget)
        if pracownik.coordinates is None:
            messagebox.showerror("Błąd", f"Nie udało się pobrać współrzędnych dla pracownika {location}.")
            return
        workers.append(pracownik)
        listbox_pracownikow.insert(tk.END, f'{name} ({location})')
        staff_name_entry.delete(0, tk.END)
        staff_location_entry.delete(0, tk.END)
        staff_theater_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Błąd", "Podaj prawidłowy numer teatru.")

def remove_client():
    selection = listbox_klientow.curselection()
    if selection:
        index = selection[0]
        if clients[index].marker:
            clients[index].marker.delete()
        clients.pop(index)
        listbox_klientow.delete(index)

def remove_worker():
    selection = listbox_pracownikow.curselection()
    if selection:
        index = selection[0]
        if workers[index].marker:
            workers[index].marker.delete()
        workers.pop(index)
        listbox_pracownikow.delete(index)

def remove_teatry():
    selection = listbox_theater.curselection()
    if selection:
        index = selection[0]
        teatr = teatry[index]

        # Usuń marker teatru z mapy
        if teatr.marker:
            teatr.marker.delete()

        # Usuń klientów związanych z teatrem
        global clients
        new_clients = []
        listbox_klientow.delete(0, tk.END)
        for klient in clients:
            if klient.theater != teatr:
                new_clients.append(klient)
                listbox_klientow.insert(tk.END, f'{klient.name} ({klient.location})')
            else:
                if klient.marker:
                    klient.marker.delete()
        clients = new_clients

        # Usuń pracowników związanych z teatrem
        global workers
        new_workers = []
        listbox_pracownikow.delete(0, tk.END)
        for pracownik in workers:
            if pracownik.theater != teatr:
                new_workers.append(pracownik)
                listbox_pracownikow.insert(tk.END, f'{pracownik.name} ({pracownik.location})')
            else:
                if pracownik.marker:
                    pracownik.marker.delete()
        workers = new_workers

        teatry.pop(index)
        listbox_theater.delete(index)

#Widoczność znaczników
def toggle_clients():
    global clients_visible
    clients_visible = not clients_visible
    for client in clients:
        if client.marker:
            if clients_visible:
                client.marker.set_visible(True)
            else:
                client.marker.set_visible(False)

def toggle_workers():
    global workers_visible
    workers_visible = not workers_visible
    for worker in workers:
        if worker.marker:
            if workers_visible:
                worker.marker.set_visible(True)
            else:
                worker.marker.set_visible(False)

def toggle_theaters():
    global theaters_visible
    theaters_visible = not theaters_visible
    for teatr in teatry:
        if teatr.marker:
            if theaters_visible:
                teatr.marker.set_visible(True)
            else:
                teatr.marker.set_visible(False)

#Pokazanie powiązanych

def show_associated():
    selection = listbox_theater.curselection()
    if not selection:
        messagebox.showinfo("Info", "Zaznacz teatr z listy.")
        return

    index = selection[0]
    teatr = teatry[index]

    # Ukryj wszystkich
    for client in clients:
        if client.marker:
            client.marker.set_visible(False)
    for worker in workers:
        if worker.marker:
            worker.marker.set_visible(False)
    for t in teatry:
        if t.marker:
            t.marker.set_visible(False)

    # Pokaż wybrany teatr
    if teatr.marker:
        teatr.marker.set_visible(True)

    # Pokaż powiązanych klientów i pracowników
    for client in clients:
        if client.theater == teatr and client.marker:
            client.marker.set_visible(True)
    for worker in workers:
        if worker.theater == teatr and worker.marker:
            worker.marker.set_visible(True)




#+#def load_sample_data():
#+#    # Dodajemy przykładowe teatry
#+#    sample_theaters = [
#+#        ("Teatr Narodowy", "Teatr_Narodowy_w_Warszawie"),
#+#        ("Teatr Wielki", "Teatr_Wielki_w_Warszawie"),
#+#        ("Teatr Polski", "Teatr_Polski_w_Warszawie")
#+#    ]
#+#    for name, wiki_location in sample_theaters:
#+#        teatr = Teatr(name, wiki_location)
#+#        if teatr.coordinates:
#+#            teatry.append(teatr)
#+#            listbox_theater.insert(tk.END, f'{name} ({wiki_location})')
#+#
#+#    # Dodajemy przykładowych pracowników (z przypisanym teatrem)
#+#    sample_workers = [
#+#        ("Jan Kowalski", "Warszawa", "aktor", 0),  # 0 to indeks teatru
#+#        ("Anna Nowak", "Warszawa", "dyrektor", 1),
#+#        ("Marek Wiśniewski", "Warszawa", "technik", 2)
#+#    ]
#+#    for name, loc, spec, theater_idx in sample_workers:
#+#        if 0 <= theater_idx < len(teatry):
#+#            pracownik = Worker(name, loc, teatry[theater_idx], specialization=spec)
#+#            if pracownik.coordinates:
#+#                workers.append(pracownik)
#+#                listbox_pracownikow.insert(tk.END, f'{name} ({loc})')
#+#
#+#    # Dodajemy przykładowych klientów
#+#    sample_clients = [
#+#        ("Krzysztof K.", "Warszawa", 0),
#+#        ("Maria Z.", "Warszawa", 1),
#+#        ("Paweł S.", "Warszawa", 2)
#+#    ]
#+#    for name, loc, theater_idx in sample_clients:
#+#        if 0 <= theater_idx < len(teatry):
#+#            klient = Client(name, loc, teatry[theater_idx])
#+#            if klient.coordinates:
#+#                clients.append(klient)
#+#                listbox_klientow.insert(tk.END, f'{name} ({loc})')


root = tk.Tk()
root.title("Mapa Teatralna")
root.geometry("1000x600")
root.minsize(800, 500)


root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Lewy panel (formularze + lista)
left_frame = ttk.Frame(root, padding=10)
left_frame.grid(row=0, column=0, sticky="ns")
left_frame.grid_rowconfigure(3, weight=1)

# Prawy panel (mapa + szczegóły)
right_frame = ttk.Frame(root, padding=10)
right_frame.grid(row=0, column=1, sticky="nsew")
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_columnconfigure(0, weight=1)

map_widget = tkintermapview.TkinterMapView(right_frame, corner_radius=0)
map_widget.grid(row=0, column=0, sticky="nsew")
map_widget.set_position(52.2297, 21.0122)
map_widget.set_zoom(6)

# Ramka na szczegóły obiektu
info_frame = ttk.Frame(right_frame)
info_frame.grid(row=1, column=0, sticky="ew", pady=10)
info_frame.columnconfigure(1, weight=1)

info_label = ttk.Label(info_frame, text="Szczegóły:", font=("Arial", 12, "bold"))
info_label.grid(row=0, column=0, columnspan=2, sticky="w")

info_name = ttk.Label(info_frame, text="name:")
info_name.grid(row=1, column=0, sticky="e")
info_name_value = ttk.Label(info_frame, text="")
info_name_value.grid(row=1, column=1, sticky="w")

info_address = ttk.Label(info_frame, text="location:")
info_address.grid(row=2, column=0, sticky="e")
info_address_value = ttk.Label(info_frame, text="")
info_address_value.grid(row=2, column=1, sticky="w")

# Klienci
client_frame = ttk.LabelFrame(left_frame, text="Klienci", padding=10)
client_frame.grid(row=0, column=0, sticky="ew", pady=2)

client_name_label = ttk.Label(client_frame, text="Imię i nazwisko klienta:")
client_name_label.grid(row=0, column=0, sticky="w")
client_name_entry = ttk.Entry(client_frame)
client_name_entry.grid(row=0, column=1, sticky="ew")

client_location_label = ttk.Label(client_frame, text="Lokalizacja klienta:")
client_location_label.grid(row=1, column=0, sticky="w")
client_location_entry = ttk.Entry(client_frame)
client_location_entry.grid(row=1, column=1, sticky="ew")

client_theater_label = ttk.Label(client_frame, text="Nr teatru:")
client_theater_label.grid(row=2, column=0, sticky="w")
client_theater_entry = ttk.Entry(client_frame)
client_theater_entry.grid(row=2, column=1, sticky="ew")

add_client_btn = ttk.Button(client_frame, text="Dodaj", compound="left", command=add_client)
add_client_btn.grid(row=3, column=0, pady=5)

remove_client_btn = ttk.Button(client_frame, text="Usuń", compound="left", command=remove_client)
remove_client_btn.grid(row=3, column=1, pady=5)

listbox_klientow = tk.Listbox(client_frame, height=4)
listbox_klientow.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)

# Pracownicy
staff_frame = ttk.LabelFrame(left_frame, text="Pracownicy", padding=10)
staff_frame.grid(row=1, column=0, sticky="ew", pady=5)

staff_name_label = ttk.Label(staff_frame, text="Imię i nazwisko pracownika:")
staff_name_label.grid(row=0, column=0, sticky="w")
staff_name_entry = ttk.Entry(staff_frame)
staff_name_entry.grid(row=0, column=1, sticky="ew")

staff_location_label = ttk.Label(staff_frame, text="Lokalizacja pracownika:")
staff_location_label.grid(row=1, column=0, sticky="w")
staff_location_entry = ttk.Entry(staff_frame)
staff_location_entry.grid(row=1, column=1, sticky="ew")

staff_theater_label = ttk.Label(staff_frame, text="Nr teatru:")
staff_theater_label.grid(row=2, column=0, sticky="w")
staff_theater_entry = ttk.Entry(staff_frame)
staff_theater_entry.grid(row=2, column=1, sticky="ew")

add_staff_btn = ttk.Button(staff_frame, text="Dodaj", compound="left", command=add_worker)
add_staff_btn.grid(row=4, column=0, pady=5)

remove_staff_btn = ttk.Button(staff_frame, text="Usuń", compound="left", command=remove_worker)
remove_staff_btn.grid(row=4, column=1, pady=5)

listbox_pracownikow = tk.Listbox(staff_frame, height=4)
listbox_pracownikow.grid(row=5, column=0, columnspan=2, sticky="ew", pady=5)

staff_specialization_label = ttk.Label(staff_frame, text="Specjalizacja:")
staff_specialization_label.grid(row=3, column=0, sticky="w")

staff_specialization_entry = ttk.Combobox(
    staff_frame, values=["Reżyser", "Właściciel", "Aktor", "Technik"], state="readonly"
)
staff_specialization_entry.grid(row=3, column=1, sticky="ew")

# Teatry
theater_frame = ttk.LabelFrame(left_frame, text="Teatry", padding=10)
theater_frame.grid(row=2, column=0, sticky="ew", pady=5)

theater_name_label = ttk.Label(theater_frame, text="name teatru:")
theater_name_label.grid(row=0, column=0, sticky="w")
theater_name_entry = ttk.Entry(theater_frame)
theater_name_entry.grid(row=0, column=1, sticky="ew")

theater_address_label = ttk.Label(theater_frame, text="location teatru (name Wikipedii):")
theater_address_label.grid(row=1, column=0, sticky="w")
theater_address_entry = ttk.Entry(theater_frame)
theater_address_entry.grid(row=1, column=1, sticky="ew")

add_theater_btn = ttk.Button(theater_frame, text="Dodaj", compound="left", command=add_teatr)
add_theater_btn.grid(row=2, column=0, pady=5)

remove_theater_btn = ttk.Button(theater_frame, text="Usuń", compound="left", command=remove_teatry)
remove_theater_btn.grid(row=2, column=1, pady=5)

listbox_theater = tk.Listbox(theater_frame, height=4)
listbox_theater.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)


#Przyciski do pokazywania i chowania

toggle_frame = ttk.Frame(theater_frame)
toggle_frame.grid(row=5, column=0, columnspan=2, pady=10)

btn_clients = ttk.Button(toggle_frame, text="Klienci", command=toggle_clients)
btn_clients.grid(row=0, column=0, padx=5)

btn_workers = ttk.Button(toggle_frame, text="Pracownicy", command=toggle_workers)
btn_workers.grid(row=0, column=1, padx=5)

btn_theaters = ttk.Button(toggle_frame, text="Teatry", command=toggle_theaters)
btn_theaters.grid(row=0, column=2, padx=5)

btn_show_associated = ttk.Button(toggle_frame, text="Pokaż powiązanych", command=show_associated)
btn_show_associated.grid(row=0, column=3, padx=5)

# Zapewnij rozciąganie kolumn wejść
for frame in (client_frame, staff_frame, theater_frame):
    frame.grid_columnconfigure(1, weight=1)

    # Dodawanie teatrów
    #-#add_teatr("Teatr Narodowy", "Warszawa")
    #-#add_teatr("Teatr Bagatela", "Kraków")
    #-#add_teatr("Teatr Nowy", "Poznań")
    #-#add_teatr("Teatr Muzyczny", "Gdynia")

    # Pracownicy Teatr Narodowy
    #-#add_worker("Jan Kowalski", "Legionowo", "Reżyser", "Teatr Narodowy")
    #-#add_worker("Anna Nowak", "Piaseczno", "Właściciel", "Teatr Narodowy")
    #-#add_worker("Marek Zieliński", "Otwock", "Technik", "Teatr Narodowy")
    #-#add_worker("Ewa Kamińska", "Ząbki", "Aktor", "Teatr Narodowy")
    #-#add_worker("Piotr Lewandowski", "Marki", "Aktor", "Teatr Narodowy")

    # Klienci Teatr Narodowy
    #-#add_client("Katarzyna Wójcik", "Mińsk Mazowiecki", "Teatr Narodowy")
    #-#add_client("Tomasz Mazur", "Grodzisk Mazowiecki", "Teatr Narodowy")
    #-#add_client("Agnieszka Kwiatkowska", "Wołomin", "Teatr Narodowy")
    #-#add_client("Robert Nowicki", "Pruszków", "Teatr Narodowy")

    # Pracownicy Teatr Bagatela
    #-#add_worker("Aleksandra Dąbrowska", "Wieliczka", "Reżyser", "Teatr Bagatela")
    #-#add_worker("Tadeusz Szymański", "Skawina", "Właściciel", "Teatr Bagatela")
    #-#add_worker("Natalia Król", "Bochnia", "Technik", "Teatr Bagatela")
    #-#add_worker("Łukasz Pawlak", "Myślenice", "Aktor", "Teatr Bagatela")
    #-#add_worker("Magdalena Czerwińska", "Niepołomice", "Aktor", "Teatr Bagatela")

    # Klienci Teatr Bagatela
    #-#add_client("Kamil Górski", "Nowy Targ", "Teatr Bagatela")
    #-#add_client("Elżbieta Lis", "Chrzanów", "Teatr Bagatela")
    #-#add_client("Grzegorz Zając", "Oświęcim", "Teatr Bagatela")
    #-#add_client("Joanna Malinowska", "Zakopane", "Teatr Bagatela")

    # Pracownicy Teatr Nowy
    #-#add_worker("Karolina Michalska", "Swarzędz", "Reżyser", "Teatr Nowy")
    #-#add_worker("Paweł Wysocki", "Luboń", "Właściciel", "Teatr Nowy")
    #-#add_worker("Marta Jabłońska", "Mosina", "Technik", "Teatr Nowy")
    #-#add_worker("Adrian Rutkowski", "Oborniki", "Aktor", "Teatr Nowy")
    #-#add_worker("Justyna Adamczyk", "Czempiń", "Aktor", "Teatr Nowy")

    # Klienci Teatr Nowy
    #-#add_client("Dominika Walczak", "Września", "Teatr Nowy")
    #-#add_client("Sebastian Chmiel", "Śrem", "Teatr Nowy")
    #-#add_client("Maria Kubicka", "Gniezno", "Teatr Nowy")
    #-#add_client("Rafał Baran", "Kościan", "Teatr Nowy")

    # Pracownicy Teatr Muzyczny
    #-#add_worker("Dorota Borkowska", "Reda", "Reżyser", "Teatr Muzyczny")
    #-#add_worker("Krzysztof Urban", "Rumia", "Właściciel", "Teatr Muzyczny")
    #-#add_worker("Beata Wróbel", "Puck", "Technik", "Teatr Muzyczny")
    #-#add_worker("Michał Nowakowski", "Kartuzy", "Aktor", "Teatr Muzyczny")
    #-#add_worker("Patrycja Grabowska", "Tczew", "Aktor", "Teatr Muzyczny")

    # Klienci Teatr Muzyczny
    #-#add_client("Zofia Tomaszewska", "Hel", "Teatr Muzyczny")
    #-#add_client("Andrzej Kowalczyk", "Nowy Dwór Gdański", "Teatr Muzyczny")
    #-#add_client("Małgorzata Piątek", "Starogard Gdański", "Teatr Muzyczny")
    #-#add_client("Emil Sawicki", "Malbork", "Teatr Muzyczny")

#-#load_sample_data()
root.mainloop()
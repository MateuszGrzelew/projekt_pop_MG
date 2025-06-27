import tkinter as tk
from tkinter import ttk, messagebox
import tkintermapview
import requests
from bs4 import BeautifulSoup

teatry = []
clients = []
workers = []


class Teatr:
    def __init__(self, teatry_name, teatry_location):
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
    def __init__(self, name, location, theater):
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
    def __init__(self, name, location, theater, specialization):
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


def add_teatr():
    name = theater_name_entry.get()
    location = theater_address_entry.get()
    teatr = Teatr(name, location)
    teatry.append(teatr)

    if not name or not location:
        messagebox.showwarning("Brak danych", "Wprowadź nazwę i lokalizację teatru.")
        return

    if teatr.coordinates is None:
        messagebox.showerror("Błąd", f"Nie udało się znaleźć współrzędnych dla lokalizacji: {location}")
        return

    listbox_theater.insert(tk.END, f'{name} ({location})')
    theater_name_entry.delete(0, tk.END)
    theater_address_entry.delete(0, tk.END)
    messagebox.showinfo("Sukces", f"Dodano teatr: {name}")


def add_client():
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
        teatr = teatry[index]  # POBIERAMY OBIEKT TEATRU
        klient = Client(name, location, teatr)  # PRZEKAZUJEMY DO KONSTRUKTORA
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


def add_worker():
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
        teatr = teatry[index]
        pracownik = Worker(name, location, teatr, specialization)
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


def toggle_clients():
    global clients_visible
    clients_visible = not clients_visible
    for client in clients:
        if clients_visible:
            if client.marker is None and client.coordinates:
                client.marker = map_widget.set_marker(*client.coordinates, text=f'Klient: {client.name}')
        else:
            if client.marker:
                client.marker.delete()
                client.marker = None


def toggle_workers():
    global workers_visible
    workers_visible = not workers_visible
    for worker in workers:
        if workers_visible:
            if worker.marker is None and worker.coordinates:
                text = f'Pracownik: {worker.name}\nSpecjalizacja: {worker.specialization}'
                worker.marker = map_widget.set_marker(*worker.coordinates, text=text)
        else:
            if worker.marker:
                worker.marker.delete()
                worker.marker = None


def toggle_theaters():
    global theaters_visible
    theaters_visible = not theaters_visible
    for teatr in teatry:
        if theaters_visible:
            if teatr.marker is None and teatr.coordinates:
                teatr.marker = map_widget.set_marker(*teatr.coordinates, text=f'Teatry: {teatr.teatry_name}')
        else:
            if teatr.marker:
                teatr.marker.delete()
                teatr.marker = None


def show_associated():
    selection = listbox_theater.curselection()
    if not selection:
        messagebox.showinfo("Brak wyboru", "Wybierz teatr z listy.")
        return
    index = selection[0]
    teatr = teatry[index]

    for client in clients:
        if client.theater == teatr and client.marker is None and client.coordinates:
            client.marker = map_widget.set_marker(*client.coordinates, text=f'Klient: {client.name}')

    for worker in workers:
        if worker.theater == teatr and worker.marker is None and worker.coordinates:
            worker.marker = map_widget.set_marker(*worker.coordinates,
                                                  text=f'Pracownik: {worker.name}\nSpecjalizacja: {worker.specialization}')


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

# Przyciski do pokazywania i chowania

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

root.mainloop()
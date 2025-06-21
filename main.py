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
    def __init__(self, name, location, theater):
        self.name = name
        self.location = location
        self.theater = theater
        self.coordinates = self.get_coordinates()
        if self.coordinates:
            self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f'Pracownik: {self.name}')
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

def dodaj_teatr():
    nazwa = theater_name_entry.get()
    adres = theater_address_entry.get()

    if not nazwa or not adres:
        messagebox.showwarning("Brak danych", "Wprowadź nazwę i adres teatru.")
        return

    teatr = Teatr(nazwa, adres)
    if teatr.coordinates is None:
        messagebox.showerror("Błąd", f"Nie udało się znaleźć współrzędnych dla adresu: {adres}")
        return

    teatry.append(teatr)
    listbox_theater.insert(tk.END, f'{nazwa} ({adres})')
    theater_name_entry.delete(0, tk.END)
    theater_address_entry.delete(0, tk.END)
    messagebox.showinfo("Sukces", f"Dodano teatr: {nazwa}")


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
        klient = Client(name, location, teatry[index])
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
    try:
        index = int(staff_theater_entry.get()) - 1
    except ValueError:
        messagebox.showwarning("Błąd", "Podaj prawidłowy numer teatru.")
        return

    if not name or not location:
        messagebox.showwarning("Brak danych", "Wprowadź imię i lokalizację pracownika.")
        return

    if 0 <= index < len(teatry):
        pracownik = Worker(name, location, teatry[index])
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

root = tk.Tk()
root.title("Mapa Teatralna")
root.geometry("1000x600")
root.minsize(800, 500)

# Wczytaj i przeskaluj ikony (upewnij się, że pliki są w tym samym katalogu co skrypt)
try:
    add_image = Image.open("add_icon.png").resize((24, 24), Image.LANCZOS)
    remove_image = Image.open("remove_icon.png").resize((24, 24), Image.LANCZOS)
    add_icon = ImageTk.PhotoImage(add_image)
    remove_icon = ImageTk.PhotoImage(remove_image)
except Exception as e:
    print("Nie znaleziono ikon add_icon.png lub remove_icon.png. Użyję przycisków tekstowych.")
    add_icon = None
    remove_icon = None

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

info_name = ttk.Label(info_frame, text="Nazwa:")
info_name.grid(row=1, column=0, sticky="e")
info_name_value = ttk.Label(info_frame, text="")
info_name_value.grid(row=1, column=1, sticky="w")

info_address = ttk.Label(info_frame, text="Adres:")
info_address.grid(row=2, column=0, sticky="e")
info_address_value = ttk.Label(info_frame, text="")
info_address_value.grid(row=2, column=1, sticky="w")

# Klienci
client_frame = ttk.LabelFrame(left_frame, text="Klienci", padding=10)
client_frame.grid(row=0, column=0, sticky="ew", pady=5)

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

add_client_btn = ttk.Button(client_frame, image=add_icon, text="Dodaj" if add_icon is None else "", compound="left", command=add_client)
add_client_btn.grid(row=3, column=0, pady=5)

remove_client_btn = ttk.Button(client_frame, image=remove_icon, text="Usuń" if remove_icon is None else "", compound="left", command=remove_client)
remove_client_btn.grid(row=3, column=1, pady=5)

listbox_klientow = tk.Listbox(client_frame, height=6)
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

add_staff_btn = ttk.Button(staff_frame, image=add_icon, text="Dodaj" if add_icon is None else "", compound="left", command=add_worker)
add_staff_btn.grid(row=3, column=0, pady=5)

remove_staff_btn = ttk.Button(staff_frame, image=remove_icon, text="Usuń" if remove_icon is None else "", compound="left", command=remove_worker)
remove_staff_btn.grid(row=3, column=1, pady=5)

listbox_pracownikow = tk.Listbox(staff_frame, height=6)
listbox_pracownikow.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)

# Teatry
theater_frame = ttk.LabelFrame(left_frame, text="Teatry", padding=10)
theater_frame.grid(row=2, column=0, sticky="ew", pady=5)

theater_name_label = ttk.Label(theater_frame, text="Nazwa teatru:")
theater_name_label.grid(row=0, column=0, sticky="w")
theater_name_entry = ttk.Entry(theater_frame)
theater_name_entry.grid(row=0, column=1, sticky="ew")

theater_address_label = ttk.Label(theater_frame, text="Adres teatru (nazwa Wikipedii):")
theater_address_label.grid(row=1, column=0, sticky="w")
theater_address_entry = ttk.Entry(theater_frame)
theater_address_entry.grid(row=1, column=1, sticky="ew")

add_theater_btn = ttk.Button(theater_frame, image=add_icon, text="Dodaj" if add_icon is None else "", compound="left", command=dodaj_teatr)
add_theater_btn.grid(row=2, column=0, pady=5)

remove_theater_btn = ttk.Button(theater_frame, image=remove_icon, text="Usuń" if remove_icon is None else "", compound="left", command=remove_teatry)
remove_theater_btn.grid(row=2, column=1, pady=5)

listbox_theater = tk.Listbox(theater_frame, height=6)
listbox_theater.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)

# Zapewnij rozciąganie kolumn wejść
for frame in (client_frame, staff_frame, theater_frame):
    frame.grid_columnconfigure(1, weight=1)

root.mainloop()
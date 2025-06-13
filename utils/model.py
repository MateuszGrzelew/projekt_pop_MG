from tkinter import *

import tinkermapview
from click import command

users: list = []


def add_user():
    zmienna_imie=entry_name.get()
    zmienna_nazwisko=entry_surname.get()
    zmienna_miejscowosc=entry_location.get()
    zmienna_posty=entry_posts.get()
    user={"name":zmienna_imie,"surname":zmienna_nazwisko,"location":zmienna_miejscowosc,"post":zmienna_posty}
    users.append(user)
    entry_name.delete(0,END)
    entry_surname.delete(0,END)
    entry_location.delete(0, END)
    entry_posts.delete(0, END)

    entry_name.focus()

def show_users():
    listbox_lista_obiektow.delete(0,END)
    for idx,user in enumerate(users):
        listbox_lista_obiektow.insert(idx,f'{idx+1}. {user["name"]} {user["surname"]}')

def remove_user():
    i=listbox_lista_obiektow.index(ACTIVE)
    users.pop(i)
    show_users()

def edit_user():
    i=listbox_lista_obiektow.index(ACTIVE)
    name=users[i]["name"]
    surname=users[i]["surname"]
    location=users[i]["location"]
    posts=users[i]["post"]

    entry_posts.insert(0,posts)
    entry_location.insert(0,location)
    entry_surname.insert(0,surname)
    entry_name.insert(0,name)

    button_dodaj_obiekt.config(text="zapisz", command=lambda: update_users)





def update_users():
    new_name=entry_name.get()
    new_surname=entry_surname.get()
    new_location=entry_location.get()
    new_posts=entry_posts.get()

    users[i]['name']=new_name
    users[i]['name']=new_surname
    users[i]['surname']=new_location
    users[i]['location']=new_location

    button_dodaj_obiekt.config(text="dodaj obiekt", command=add_users)
    show_users()

def my_function():
    my_label.config(text="Hello World")

def show_user_details():
    i=listbox_lista_obiektow.index(ACTIVE)
    name=users[i]["name"]
    surname=users[i]["surname"]
    location=users[i]["location"]
    posts=users[i]["post"]
    label_szczegoly_name_wartosc.config(text=name)
    label_szczegoly_surname_wartosc.config(text=surname)
    label_szczegoly_location_wartosc.config(text=location)
    label_szczegoly_posts_wartosc.config(text=posts)

root = Tk()
root.geometry("1200x760")
root.title("Map Book")

ramka_lista_obiektow=Frame(root)
ramka_formularz=Frame(root)
ramka_szczegoly_obiektow = Frame(root)
ramka_mapa=Frame(root)

ramka_lista_obiektow.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_obiektow.grid(row=1, column=0, columnspan=2)
ramka_mapa.grid(row=2, column=0, columnspan=2)

# ramka_lista_obiektow
label_lista_obiektow=Label(ramka_lista_obiektow, text="Lista użytkowników")
label_lista_obiektow.grid(row=0, column=0, columnspan=3)
listbox_lista_obiektow=Listbox(ramka_lista_obiektow, width=50, height=10)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly_obiektow=Button(ramka_lista_obiektow,text="pokaz szczegoly")
button_pokaz_szczegoly_obiektow.grid(row=2, column=0)
button_usun_obiekt=Button(ramka_lista_obiektow,text="usuń obiekt", commandremove_user))
button_usun_obiekt.grid(row=2, column=1)
button_edytuj_obiekt=Button(ramka_lista_obiektow,text="edytuj obiekt")
button_edytuj_obiekt.grid(row=2, column=2)

# ramka_formularz
label_formularz=Label(ramka_formularz, text="Formularz")
label_formularz.grid(row=0, column=0, columnspan=2)
label_name=Label(ramka_formularz, text="Name")
label_name.grid(row=1, column=0, sticky=W)
label_surname=Label(ramka_formularz, text="Surname")
label_surname.grid(row=2, column=0, sticky=W)
label_location=Label(ramka_formularz, text="Location")
label_location.grid(row=3, column=0, sticky=W)
label_posts=Label(ramka_formularz, text="Posts")
label_posts.grid(row=4, column=0, sticky=W)

entry_name=Entry(ramka_formularz)
entry_name.grid(row=1, column=1)
entry_surname=Entry(ramka_formularz)
entry_surname.grid(row=2, column=1)
entry_location=Entry(ramka_formularz)
entry_location.grid(row=3, column=1)
entry_posts=Entry(ramka_formularz)
entry_posts.grid(row=4, column=1)

button_dodaj_obiekt=Button(ramka_formularz,text="dodaj obiekt")
button_dodaj_obiekt.grid(row=5, column=0, columnspan=2)

# ramka_szczegoly_obiektow
label_szczegoly_obiektow=Label(ramka_szczegoly_obiektow, text="Szczegóły obiektów")
label_szczegoly_obiektow.grid(row=0, column=0,)
label_szczegoly_name=Label(ramka_szczegoly_obiektow, text="Name")
label_szczegoly_name.grid(row=1, column=0,)
label_szczegoly_name_wartosc=Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_name_wartosc.grid(row=1, column=1,)
label_szczegoly_surname=Label(ramka_szczegoly_obiektow, text="Surname")
label_szczegoly_surname.grid(row=1, column=2,)
label_szczegoly_surname_wartosc=Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_surname_wartosc.grid(row=1, column=3,)
label_szczegoly_location=Label(ramka_szczegoly_obiektow, text="Location")
label_szczegoly_location.grid(row=1, column=4,)
label_szczegoly_location_wartosc=Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_location_wartosc.grid(row=1, column=5,)
label_szczegoly_posts=Label(ramka_szczegoly_obiektow, text="Posts")
label_szczegoly_posts.grid(row=1, column=6,)
label_szczegoly_posts_wartosc=Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_posts_wartosc.grid(row=1, column=7,)

# ramka_mapa
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=500, corner_radius=5)
map_widget.grid(row=0, column=0, columnspan=2)
map_widget.setposition(52.23, 21.0)
map_widget.setzoom(6.0)




root.mainloop()

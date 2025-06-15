from tkinter import *
from tkinter import ttk
import tkintermapview
import requests
from bs4 import BeautifulSoup

class Bar:
    def __init__(self, name, location, rating, map_widget):
        self.name = name
        self.location = location
        self.rating = rating
        self.map_widget = map_widget
        self.coordinates = self.get_coordinates()
        self.marker = self.map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f'{self.name} {self.rating}')

    def get_coordinates(self):
        try:
            adres_url = f'https://pl.wikipedia.org/wiki/{self.location}'
            response_html = BeautifulSoup(requests.get(adres_url).content, 'html.parser')
            return [
                float(response_html.select('.latitude')[1].text.replace(',', '.')),
                float(response_html.select('.longitude')[1].text.replace(',', '.')),
            ]
        except Exception as e:
            print("Błąd pobierania współrzędnych:", e)
            return [52.23, 21.00]


class Client:
    def __init__(self, bar_name, client_name, client_surname, location, visits, map_widget):
        self.bar_name = bar_name
        self.client_name = client_name
        self.client_surname = client_surname
        self.location = location
        self.visits = visits
        self.map_widget = map_widget
        self.coordinates = self.get_coordinates()
        self.marker = self.map_widget.set_marker(
            self.coordinates[0], self.coordinates[1],
            text=f'{self.bar_name}: {self.client_name} {self.client_surname}'
        )

    def get_coordinates(self):
        try:
            adres_url = f'https://pl.wikipedia.org/wiki/{self.location}'
            response_html = BeautifulSoup(requests.get(adres_url).content, 'html.parser')
            return [
                float(response_html.select('.latitude')[1].text.replace(',', '.')),
                float(response_html.select('.longitude')[1].text.replace(',', '.')),
            ]
        except Exception as e:
            print("Błąd pobierania współrzędnych:", e)
            return [52.23, 21.00]


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("System zarządzania siecią barów")
        self.root.geometry("1200x700")

        self.bars = []
        self.clients = []

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        self.frame_bars = Frame(self.notebook)
        self.notebook.add(self.frame_bars, text='Bary')

        self.frame_clients = Frame(self.notebook)
        self.notebook.add(self.frame_clients, text='Klienci')

        self.setup_bars_tab()
        self.setup_clients_tab()

    def setup_bars_tab(self):
        frame_list = Frame(self.frame_bars)
        frame_list.grid(row=0, column=0, padx=10, pady=10, sticky='n')

        Label(frame_list, text="Lista barów:").pack()
        self.listbox_bars = Listbox(frame_list, width=50, height=10)
        self.listbox_bars.pack()

        Button(frame_list, text="Pokaż szczegóły", command=self.show_bar_details).pack(side=LEFT, padx=5, pady=5)
        Button(frame_list, text="Usuń", command=self.remove_bar).pack(side=LEFT, padx=5, pady=5)
        Button(frame_list, text="Edytuj", command=self.edit_bar).pack(side=LEFT, padx=5, pady=5)

        frame_form = Frame(self.frame_bars)
        frame_form.grid(row=0, column=1, padx=10, pady=10, sticky='n')

        Label(frame_form, text="Formularz dodawania baru").grid(row=0, column=0, columnspan=2)

        Label(frame_form, text="Nazwa:").grid(row=1, column=0, sticky=W)
        self.entry_bar_name = Entry(frame_form)
        self.entry_bar_name.grid(row=1, column=1)

        Label(frame_form, text="Miejscowość:").grid(row=2, column=0, sticky=W)
        self.entry_bar_location = Entry(frame_form)
        self.entry_bar_location.grid(row=2, column=1)

        Label(frame_form, text="Ocena:").grid(row=3, column=0, sticky=W)
        self.entry_bar_rating = Entry(frame_form)
        self.entry_bar_rating.grid(row=3, column=1)

        self.btn_add_bar = Button(frame_form, text="Dodaj", command=self.add_bar)
        self.btn_add_bar.grid(row=4, column=0, columnspan=2, pady=5)

        frame_details = Frame(self.frame_bars)
        frame_details.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='w')

        Label(frame_details, text="Szczegóły baru:").grid(row=0, column=0, columnspan=6)

        Label(frame_details, text="Nazwa:").grid(row=1, column=0)
        self.label_bar_detail_name = Label(frame_details, text="...")
        self.label_bar_detail_name.grid(row=1, column=1)

        Label(frame_details, text="Miejscowość:").grid(row=1, column=2)
        self.label_bar_detail_location = Label(frame_details, text="...")
        self.label_bar_detail_location.grid(row=1, column=3)

        Label(frame_details, text="Ocena:").grid(row=1, column=4)
        self.label_bar_detail_rating = Label(frame_details, text="...")
        self.label_bar_detail_rating.grid(row=1, column=5)

        self.map_bars = tkintermapview.TkinterMapView(self.frame_bars, width=1200, height=400)
        self.map_bars.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.map_bars.set_position(52.23, 21.00)
        self.map_bars.set_zoom(6)

    def setup_clients_tab(self):
        frame_list = Frame(self.frame_clients)
        frame_list.grid(row=0, column=0, padx=10, pady=10, sticky='n')

        Label(frame_list, text="Lista klientów:").pack()
        self.listbox_clients = Listbox(frame_list, width=50, height=10)
        self.listbox_clients.pack()

        Button(frame_list, text="Pokaż szczegóły", command=self.show_client_details).pack(side=LEFT, padx=5, pady=5)
        Button(frame_list, text="Usuń", command=self.remove_client).pack(side=LEFT, padx=5, pady=5)
        Button(frame_list, text="Edytuj", command=self.edit_client).pack(side=LEFT, padx=5, pady=5)

        frame_form = Frame(self.frame_clients)
        frame_form.grid(row=0, column=1, padx=10, pady=10, sticky='n')

        Label(frame_form, text="Formularz dodawania klienta").grid(row=0, column=0, columnspan=2)

        self.entry_client_bar = Entry(frame_form)
        self.entry_client_name = Entry(frame_form)
        self.entry_client_surname = Entry(frame_form)
        self.entry_client_location = Entry(frame_form)
        self.entry_client_visits = Entry(frame_form)

        labels = ["Bar:", "Imię:", "Nazwisko:", "Miejscowość:", "Liczba wizyt:"]
        entries = [self.entry_client_bar, self.entry_client_name, self.entry_client_surname, self.entry_client_location,
                   self.entry_client_visits]

        for i, (label, entry) in enumerate(zip(labels, entries), start=1):
            Label(frame_form, text=label).grid(row=i, column=0, sticky=W)
            entry.grid(row=i, column=1)

        self.btn_add_client = Button(frame_form, text="Dodaj", command=self.add_client)
        self.btn_add_client.grid(row=6, column=0, columnspan=2, pady=5)

        frame_details = Frame(self.frame_clients)
        frame_details.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='w')

        Label(frame_details, text="Szczegóły klienta:").grid(row=0, column=0, columnspan=6)

        detail_labels = ["Bar:", "Imię:", "Nazwisko:", "Miejscowość:", "Liczba wizyt:"]
        self.detail_vars_clients = [Label(frame_details, text="...") for _ in detail_labels]
        for i, (label, var) in enumerate(zip(detail_labels, self.detail_vars_clients)):
            Label(frame_details, text=label).grid(row=1, column=i * 2, padx=5, pady=5)
            var.grid(row=1, column=i * 2 + 1, padx=5, pady=5)

        self.map_clients = tkintermapview.TkinterMapView(self.frame_clients, width=1200, height=400)
        self.map_clients.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.map_clients.set_position(52.23, 21.00)
        self.map_clients.set_zoom(6)


    def add_bar(self):
        name = self.entry_bar_name.get()
        location = self.entry_bar_location.get()
        rating = self.entry_bar_rating.get()
        if not name or not location or not rating:
            return
        bar = Bar(name, location, rating, self.map_bars)
        self.bars.append(bar)
        self.listbox_bars.insert(END, f"{bar.name}")
        for entry in [self.entry_bar_name, self.entry_bar_location, self.entry_bar_rating]:
            entry.delete(0, END)

    def show_bar_details(self):
        i = self.listbox_bars.curselection()
        if not i: return
        bar = self.bars[i[0]]
        self.label_bar_detail_name.config(text=bar.name)
        self.label_bar_detail_location.config(text=bar.location)
        self.label_bar_detail_rating.config(text=bar.rating)
        self.map_bars.set_position(*bar.coordinates)
        self.map_bars.set_zoom(15)

    def remove_bar(self):
        i = self.listbox_bars.curselection()
        if not i: return
        bar = self.bars.pop(i[0])
        bar.marker.delete()
        self.listbox_bars.delete(i)

    def edit_bar(self):
        i = self.listbox_bars.curselection()
        if not i: return
        bar = self.bars[i[0]]
        self.entry_bar_name.delete(0, END); self.entry_bar_name.insert(0, bar.name)
        self.entry_bar_location.delete(0, END); self.entry_bar_location.insert(0, bar.location)
        self.entry_bar_rating.delete(0, END); self.entry_bar_rating.insert(0, bar.rating)
        self.btn_add_bar.config(text="Zapisz", command=lambda idx=i[0]: self.update_bar(idx))

    def update_bar(self, idx):
        name = self.entry_bar_name.get()
        location = self.entry_bar_location.get()
        rating = self.entry_bar_rating.get()
        bar = self.bars[idx]
        bar.name = name
        bar.location = location
        bar.rating = rating
        bar.coordinates = bar.get_coordinates()
        bar.marker.delete()
        bar.marker = self.map_bars.set_marker(*bar.coordinates, text=f"{bar.name} {bar.rating}")
        self.listbox_bars.delete(idx)
        self.listbox_bars.insert(idx, bar.name)
        self.btn_add_bar.config(text="Dodaj", command=self.add_bar)
        for entry in [self.entry_bar_name, self.entry_bar_location, self.entry_bar_rating]:
            entry.delete(0, END)

    def add_client(self):
        bar = self.entry_client_bar.get()
        name = self.entry_client_name.get()
        surname = self.entry_client_surname.get()
        location = self.entry_client_location.get()
        visits = self.entry_client_visits.get()
        if not bar or not name or not surname or not location or not visits:
            return
        client = Client(bar, name, surname, location, visits, self.map_clients)
        self.clients.append(client)
        self.listbox_clients.insert(END, f"{name} {surname}")
        for entry in [self.entry_client_bar, self.entry_client_name, self.entry_client_surname,
                      self.entry_client_location, self.entry_client_visits]:
            entry.delete(0, END)

    def show_client_details(self):
        i = self.listbox_clients.curselection()
        if not i: return
        c = self.clients[i[0]]
        texts = [c.bar_name, c.client_name, c.client_surname, c.location, c.visits]
        for lbl, txt in zip(self.detail_vars_clients, texts):
            lbl.config(text=txt)
        self.map_clients.set_position(*c.coordinates)
        self.map_clients.set_zoom(15)

    def remove_client(self):
        i = self.listbox_clients.curselection()
        if not i: return
        c = self.clients.pop(i[0])
        c.marker.delete()
        self.listbox_clients.delete(i)

    def edit_client(self):
        i = self.listbox_clients.curselection()
        if not i: return
        c = self.clients[i[0]]
        self.entry_client_bar.delete(0, END);
        self.entry_client_bar.insert(0, c.bar_name)
        self.entry_client_name.delete(0, END);
        self.entry_client_name.insert(0, c.client_name)
        self.entry_client_surname.delete(0, END);
        self.entry_client_surname.insert(0, c.client_surname)
        self.entry_client_location.delete(0, END);
        self.entry_client_location.insert(0, c.location)
        self.entry_client_visits.delete(0, END);
        self.entry_client_visits.insert(0, c.visits)
        self.btn_add_client.config(text="Zapisz", command=lambda idx=i[0]: self.update_client(idx))

    def update_client(self, idx):
        c = self.clients[idx]
        c.bar_name = self.entry_client_bar.get()
        c.client_name = self.entry_client_name.get()
        c.client_surname = self.entry_client_surname.get()
        c.location = self.entry_client_location.get()
        c.visits = self.entry_client_visits.get()
        c.coordinates = c.get_coordinates()
        c.marker.delete()
        c.marker = self.map_clients.set_marker(*c.coordinates, text=f"{c.bar_name}: {c.client_name} {c.client_surname}")
        self.listbox_clients.delete(idx)
        self.listbox_clients.insert(idx, f"{c.client_name} {c.client_surname}")
        self.btn_add_client.config(text="Dodaj", command=self.add_client)
        for entry in [self.entry_client_bar, self.entry_client_name, self.entry_client_surname,
                      self.entry_client_location, self.entry_client_visits]:
            entry.delete(0, END)


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
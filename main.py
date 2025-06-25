from tkinter import *
from tkinter import ttk, messagebox
import tkintermapview
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

def get_coordinates_from_wikipedia(location):
    try:
        adres_url = f'https://pl.wikipedia.org/wiki/{location}'
        response_html = BeautifulSoup(requests.get(adres_url).content, 'html.parser')
        latitude = float(response_html.select('.latitude')[1].text.replace(',', '.'))
        longitude = float(response_html.select('.longitude')[1].text.replace(',', '.'))
        return [latitude, longitude]
    except Exception as e:
        print("Błąd pobierania współrzędnych:", e)
        return [52.23, 21.00]

class Bar:
    def __init__(self, name, location, rating, map_widget):
        self.name = name
        self.location = location
        self.rating = rating
        self.map_widget = map_widget
        self.coordinates = get_coordinates_from_wikipedia(self.location)
        self.marker = self.map_widget.set_marker(self.coordinates[0], self.coordinates[1],
                                                 text=f'{self.name} {self.rating}')

class Client:
    def __init__(self, bar_name, client_name, client_surname, location, visits, map_widget):
        self.bar_name = bar_name
        self.client_name = client_name
        self.client_surname = client_surname
        self.location = location
        self.visits = visits
        self.map_widget = map_widget
        self.coordinates = get_coordinates_from_wikipedia(self.location)
        self.marker = self.map_widget.set_marker(
            self.coordinates[0], self.coordinates[1],
            text=f'{self.bar_name}: {self.client_name} {self.client_surname}'
        )

class Employee:
    def __init__(self, bar_name, employee_name, employee_surname, location, years_of_work, map_widget):
        self.bar_name = bar_name
        self.employee_name = employee_name
        self.employee_surname = employee_surname
        self.location = location
        self.years_of_work = years_of_work
        self.map_widget = map_widget
        self.coordinates = get_coordinates_from_wikipedia(self.location)
        self.marker = self.map_widget.set_marker(
            self.coordinates[0], self.coordinates[1],
            text=f'{self.bar_name}: {self.employee_name} {self.employee_surname}'
        )


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("System zarządzania siecią barów")
        self.root.geometry("1200x700")

        self.bars = []
        self.clients = []
        self.employees = []

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        self.frame_bars = Frame(self.notebook)
        self.notebook.add(self.frame_bars, text='Bary')

        self.frame_clients = Frame(self.notebook)
        self.notebook.add(self.frame_clients, text='Klienci')

        self.frame_employees = Frame(self.notebook)
        self.notebook.add(self.frame_employees, text='Pracownicy')

        self.setup_bars_tab()
        self.setup_clients_tab()
        self.setup_employees_tab()

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

    def setup_employees_tab(self):
        frame_list = Frame(self.frame_employees)
        frame_list.grid(row=0, column=0, padx=10, pady=10, sticky='n')

        Label(frame_list, text="Lista pracowników:").pack()
        self.listbox_employees = Listbox(frame_list, width=50, height=10)
        self.listbox_employees.pack()

        Button(frame_list, text="Pokaż wszystkich pracowników", command=self.show_all_employees).pack(side=LEFT, padx=6, pady=6)
        Button(frame_list, text="Pokaż szczegóły", command=self.show_employee_details).pack(side=LEFT, padx=5, pady=5)
        Button(frame_list, text="Usuń", command=self.remove_employee).pack(side=LEFT, padx=5, pady=5)
        Button(frame_list, text="Edytuj", command=self.edit_employee).pack(side=LEFT, padx=5, pady=5)

        frame_form = Frame(self.frame_employees)
        frame_form.grid(row=0, column=1, padx=10, pady=10, sticky='n')

        Label(frame_form, text="Formularz dodawania pracownika").grid(row=0, column=0, columnspan=2)

        self.entry_employee_bar = Entry(frame_form)
        self.entry_employee_name = Entry(frame_form)
        self.entry_employee_surname = Entry(frame_form)
        self.entry_employee_location = Entry(frame_form)
        self.entry_employee_years_of_work = Entry(frame_form)



        labels = ["Bar:", "Imię:", "Nazwisko:", "Miejscowość:", "Lata pracy:"]
        entries = [self.entry_employee_bar, self.entry_employee_name, self.entry_employee_surname, self.entry_employee_location, self.entry_employee_years_of_work]

        for i, (label, entry) in enumerate(zip(labels, entries), start=1):
            Label(frame_form, text=label).grid(row=i, column=0, sticky=W)
            entry.grid(row=i, column=1)

        self.btn_add_employee = Button(frame_form, text="Dodaj", command=self.add_employee)
        self.btn_add_employee.grid(row=6, column=0, columnspan=2, pady=5)

        frame_details = Frame(self.frame_employees)
        frame_details.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='w')

        Label(frame_details, text="Szczegóły pracownika:").grid(row=0, column=0, columnspan=6)

        detail_labels = ["Bar:", "Imię:", "Nazwisko:", "Miejscowość:", "Lata pracy:"]
        self.detail_vars_employees = [Label(frame_details, text="...") for _ in detail_labels]
        for i, (label, var) in enumerate(zip(detail_labels, self.detail_vars_employees)):
            Label(frame_details, text=label).grid(row=1, column=i * 2, padx=5, pady=5)
            var.grid(row=1, column=i * 2 + 1, padx=5, pady=5)

        self.map_employees = tkintermapview.TkinterMapView(self.frame_employees, width=1200, height=400)
        self.map_employees.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.map_employees.set_position(52.23, 21.00)
        self.map_employees.set_zoom(6)

    def add_bar(self):
        name = self.entry_bar_name.get().strip()
        loc = self.entry_bar_location.get().strip()
        rating = self.entry_bar_rating.get().strip()

        if not name or not loc or not rating:
            messagebox.showwarning("Błąd", "Wypełnij wszystkie pola (nazwa, lokalizacja, ocena).")
            return

        try:
            rating = int(rating)
            if not (1 <= rating <= 5):
                raise ValueError("Ocena spoza zakresu")

            bar = Bar(name, loc, rating, self.map_bars)
            self.bars.append(bar)
            self.listbox_bars.insert(END, name)

            self.entry_bar_name.delete(0, END)
            self.entry_bar_location.delete(0, END)
            self.entry_bar_rating.delete(0, END)
        except Exception as e:
            messagebox.showwarning("Błąd", f"Nieprawidłowe dane lub lokalizacja.\n{e}")

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
        if not i:
            return
        bar = self.bars.pop(i[0])
        bar.marker.delete()
        self.listbox_bars.delete(i)

        self.label_bar_detail_name.config(text="...")
        self.label_bar_detail_location.config(text="...")
        self.label_bar_detail_rating.config(text="...")

    def edit_bar(self):
        i = self.listbox_bars.curselection()
        if not i: return
        bar = self.bars[i[0]]
        self.entry_bar_name.delete(0, END);
        self.entry_bar_name.insert(0, bar.name)
        self.entry_bar_location.delete(0, END);
        self.entry_bar_location.insert(0, bar.location)
        self.entry_bar_rating.delete(0, END);
        self.entry_bar_rating.insert(0, bar.rating)
        self.btn_add_bar.config(text="Zapisz", command=lambda idx=i[0]: self.update_bar(idx))

    def update_bar(self, idx):
        name = self.entry_bar_name.get()
        location = self.entry_bar_location.get()
        rating = self.entry_bar_rating.get()
        bar = self.bars[idx]
        bar.name = name
        bar.location = location
        bar.rating = rating
        bar.coordinates = get_coordinates_from_wikipedia(bar.location)
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
        if not i:
            return
        c = self.clients.pop(i[0])
        c.marker.delete()
        self.listbox_clients.delete(i)

        for lbl in self.detail_vars_clients:
            lbl.config(text="...")

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
        c.coordinates = get_coordinates_from_wikipedia(c.location)
        c.marker.delete()
        c.marker = self.map_clients.set_marker(*c.coordinates, text=f"{c.bar_name}: {c.client_name} {c.client_surname}")
        self.listbox_clients.delete(idx)
        self.listbox_clients.insert(idx, f"{c.client_name} {c.client_surname}")
        self.btn_add_client.config(text="Dodaj", command=self.add_client)
        for entry in [self.entry_client_bar, self.entry_client_name, self.entry_client_surname,
                      self.entry_client_location, self.entry_client_visits]:
            entry.delete(0, END)


    def add_employee(self):
        bar = self.entry_employee_bar.get()
        name = self.entry_employee_name.get()
        surname = self.entry_employee_surname.get()
        location = self.entry_employee_location.get()
        years_of_work = self.entry_employee_years_of_work.get()
        if not bar or not name or not surname or not location or not years_of_work:
            return
        employee = Employee(bar, name, surname, location, years_of_work, self.map_employees)
        self.employees.append(employee)
        self.listbox_employees.insert(END, f"{name} {surname}")
        for entry in [self.entry_employee_bar, self.entry_employee_name, self.entry_employee_surname,
                      self.entry_employee_location, self.entry_employee_years_of_work]:
            entry.delete(0, END)


    def show_employee_details(self):
        i = self.listbox_employees.curselection()
        if not i: return
        c = self.employees[i[0]]
        texts = [c.bar_name, c.employee_name, c.employee_surname, c.location, c.years_of_work]
        for lbl, txt in zip(self.detail_vars_employees, texts):
            lbl.config(text=txt)
        self.map_employees.set_position(*c.coordinates)
        self.map_employees.set_zoom(15)

    def remove_employee(self):
        i = self.listbox_employees.curselection()
        if not i:
            return
        employee = self.employees.pop(i[0])
        employee.marker.delete()
        self.listbox_employees.delete(i)

        for lbl in self.detail_vars_employees:
            lbl.config(text="...")

    def edit_employee(self):
        i = self.listbox_employees.curselection()
        if not i: return
        c = self.employees[i[0]]
        self.entry_employee_bar.delete(0, END);
        self.entry_employee_bar.insert(0, c.bar_name)
        self.entry_employee_name.delete(0, END);
        self.entry_employee_name.insert(0, c.employee_name)
        self.entry_employee_surname.delete(0, END);
        self.entry_employee_surname.insert(0, c.employee_surname)
        self.entry_employee_location.delete(0, END);
        self.entry_employee_location.insert(0, c.location)
        self.entry_employee_years_of_work.delete(0, END);
        self.entry_employee_years_of_work.insert(0, c.years_of_work)
        self.btn_add_employee.config(text="Zapisz", command=lambda idx=i[0]: self.update_employee(idx))


    def update_employee(self, idx):
        c = self.employees[idx]
        c.bar_name = self.entry_employee_bar.get()
        c.employee_name = self.entry_employee_name.get()
        c.employee_surname = self.entry_employee_surname.get()
        c.location = self.entry_employee_location.get()
        c.years_of_work = self.entry_employee_years_of_work.get()
        c.coordinates = get_coordinates_from_wikipedia(c.location)
        c.marker.delete()
        c.marker = self.map_employees.set_marker(*c.coordinates,
                                                 text=f"{c.bar_name}: {c.employee_name} {c.employee_surname}")
        self.listbox_employees.delete(idx)
        self.listbox_employees.insert(idx, f"{c.employee_name} {c.employee_surname}")
        self.btn_add_employee.config(text="Dodaj", command=self.add_employee)
        for entry in [self.entry_employee_bar, self.entry_employee_name, self.entry_employee_surname,
                      self.entry_employee_location, self.entry_employee_years_of_work]:
            entry.delete(0, END)

    def show_all_employees(self):
        # Usuń istniejące markery
        for emp in self.employees:
            if emp.marker:
                emp.marker.delete()

        # Grupowanie pracowników po barze i lokalizacji
        grouped = {}
        for emp in self.employees:
            key = (emp.bar_name, emp.location)
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(emp)

        for (bar_name, location), employees in grouped.items():
            coords = get_coordinates_from_wikipedia(location)
            # Zbuduj wieloliniowy tekst z imionami i nazwiskami
            text = f"{bar_name}:\n" + "\n".join(
                f"{emp.employee_name} {emp.employee_surname}" for emp in employees
            )
            # Ustaw jeden marker z wieloma nazwiskami
            marker = self.map_employees.set_marker(*coords, text=text)
            for emp in employees:
                emp.marker = marker  # przypisz marker do każdego, jeśli potrzebne


root = Tk()
app = App(root)
root.mainloop()

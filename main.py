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


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("System zarządzania siecią barów")
        self.root.geometry("1200x700")

        self.bars = []

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        self.frame_bars = Frame(self.notebook)
        self.notebook.add(self.frame_bars, text='Bary')

        self.setup_bars_tab()

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



if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
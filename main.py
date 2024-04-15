import csv
import re
import os
import tkinter as tk
from tkinter import Label, Entry, Button, messagebox, scrolledtext


CSV_FILE_PATH = os.path.join(".", "_internal", "DB", "Tiristory.csv")
ICON_FILE = os.path.join(".", "_internal", "logo", "logo.ico")


class TiristoryDirectoryApp(tk.Tk):
    def __init__(self, storage: list[dict]):
        super().__init__()
        self.title('Справочник тиристоров')
        self.geometry('640x550')
        self.iconbitmap(ICON_FILE)
        self.storage = storage

        Label(self, text="Введите наименование тиристора:").pack(pady=10)
        self.search_entry = Entry(self, width=50)
        self.search_entry.pack(pady=10)

        Button(self, text="Поиск", command=self.search_tiristor).pack(pady=10)

        self.results_text = scrolledtext.ScrolledText(self, width=70, height=30)
        self.results_text.pack(pady=20)

    def search_tiristor(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            messagebox.showinfo("Ошибка", "Введите значение для поиска!")
            return

        pattern = re.compile(f"^{query}$", flags=2)
        found_tiristors = [
            tiristor for tiristor in self.storage
            if re.match(pattern, tiristor["Наименование тиристора"])
        ]

        self.results_text.delete('1.0', tk.END)
        if found_tiristors:
            for tiristor in found_tiristors:
                for key, value in tiristor.items():
                    self.results_text.insert(tk.END, f"{key}: {value}\n")
                self.results_text.insert(tk.END, "-" * 60 + "\n")
        else:
            messagebox.showinfo("Результат", "Указанное наименование отсутствует!")


def add_item_from_csv(storage: list):
    with open(CSV_FILE_PATH, "r", encoding="utf-8") as fi:
        csv_reader = csv.DictReader(fi, delimiter=",", dialect="excel")
        for line in csv_reader:
            storage.append(line)


if __name__ == '__main__':
    tiristors: list = []
    add_item_from_csv(tiristors)
    app = TiristoryDirectoryApp(storage=tiristors)
    app.mainloop()

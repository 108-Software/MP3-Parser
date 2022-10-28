import os
import tkinter as tk
import sqlite3 as sql
import tkinter.ttk as ttk
from tinytag import TinyTag


class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings

        for head in headings:
            table.heading(head, text=head, anchor=tk.CENTER)
            table.column(head, anchor=tk.CENTER)

        for row in rows:
            table.insert('', tk.END, values=tuple(row))

        scrolltable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)


def parsing():

    traks = []

    for root, dirs, files, in os.walk("C:\Музыка"):
        for name in files:
            if name.endswith((".mp3", ".m4a", ".flac", "alac")):
                traks.append(name)
                temp_track = TinyTag.get(root + "\\" + name)
                database(temp_track.artist, temp_track.title, temp_track.album, temp_track.genre)


def database(artist, title, album, genre):
    con = sql.connect('test.db')
    with con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS test(
            'Группа' TEXT,
            'Название композиции' TEXT,
            'Альбом' TEXT,
            'Жанр' TEXT);
            """)
        music = (artist, title, album, genre)
        cur.execute("INSERT INTO test VALUES(?, ?, ?, ?);", music)
        con.commit()
        cur.close()


def main():
    data = ("",)
    with sql.connect('test.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM test")
        cursor.execute("SELECT * FROM test")
        data = (row for row in cursor.fetchall())

    root = tk.Tk()
    root.title("Парсер MP3")
    root.geometry("900x600")
    table = Table(root, headings=('Группа', 'Название композиции', 'Альбом', 'Жанр'), rows=data)
    table.pack(expand=tk.YES, fill=tk.BOTH, pady=50, padx=50)
    root.mainloop()


if __name__ == '__main__':
    parsing()
    main()

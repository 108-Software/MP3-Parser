import os
import Table
import tkinter as tk
import sqlite3 as sql
from tinytag import TinyTag


def parsing():

    try:
        for root, dirs, files, in os.walk("C:\Music"):
            for name in files:
                if name.endswith((".mp3", ".m4a", ".flac", "alac")):
                    try:
                        temp_track = TinyTag.get(root + "\\" + name)
                        database(temp_track.artist, temp_track.title, temp_track.album, temp_track.genre)
                    except TinyTag:
                        print("Error")
    except FileNotFoundError:
        print("В этой папке нет нужных файлов")


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
        data = (row for row in cursor.fetchall())

    root = tk.Tk()
    root.title("Парсер MP3")
    root.geometry("900x600")
    table = Table.Table(root, headings=('Группа', 'Название композиции', 'Альбом', 'Жанр'), rows=data)
    table.pack(expand=tk.YES, fill=tk.BOTH, pady=50, padx=50)
    root.mainloop()


if __name__ == '__main__':
    parsing()
    main()
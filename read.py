import inquirer
from inquirer.themes import BlueComposure
from prettytable import PrettyTable
from colorama import Fore, Style
import storage
from storage import katalog, playlist
import os

def tampilkan_menu_awal():
    os.system("cls" if os.name == "nt" else "clear")
    pertanyaan = [
        inquirer.List(
            "pilihan",
            message="=== MENU AWAL ===",
            choices=[
                "1. Login",
                "2. Registrasi",
                "3. Keluar"
            ]
        )
    ]
    jawaban = inquirer.prompt(pertanyaan, theme=BlueComposure())
    if jawaban is None:
        raise KeyboardInterrupt

    pilihan = jawaban["pilihan"]
    return pilihan[0]

def tampilkan_katalog():
    print(Fore.CYAN + "\n=== KATALOG LAGU ===")
    if len(katalog) == 0:
        print(Style.DIM + "Katalog masih kosong.")
    else:
        tabel = PrettyTable()
        tabel.field_names = ["ID", "Judul", "Penyanyi", "Genre"]
        for id_lagu in katalog:
            tabel.add_row([id_lagu, katalog[id_lagu]["judul"], katalog[id_lagu]["penyanyi"], katalog[id_lagu]["genre"]])
        print(Fore.LIGHTCYAN_EX + str(tabel))

def tampilkan_playlist_user():
    print(Fore.CYAN + "\n=== PLAYLIST SAYA ===")

    username = storage.username_aktif

    if username not in playlist or len(playlist[username]) == 0:
        print(Style.DIM + "Kamu belum membuat playlist.")
        return

    for nama_playlist in playlist[username]:
        print(Fore.MAGENTA + f"\n=== PLAYLIST: {nama_playlist} ===")

        daftar_lagu = playlist[username][nama_playlist]

        if len(daftar_lagu) == 0:
            print(Style.DIM + "Playlist Anda belum ada lagu.")
        else:
            tabel = PrettyTable()
            tabel.field_names = ["ID", "Judul", "Penyanyi", "Genre"]

            for id_lagu in daftar_lagu:
                if id_lagu in katalog:
                    data = katalog[id_lagu]

                    tabel.add_row([
                        id_lagu,
                        data["judul"],
                        data["penyanyi"],
                        data["genre"]
                    ])

            if len(tabel.rows) > 0:
                print(Fore.LIGHTCYAN_EX + str(tabel))
            else:
                print(Style.DIM + "Tidak ada lagu yang tersedia di katalog.")
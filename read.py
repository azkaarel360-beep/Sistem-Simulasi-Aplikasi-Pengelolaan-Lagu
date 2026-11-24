import inquirer
from inquirer.themes import BlueComposure
from prettytable import PrettyTable
import storage 
import KOLOR as K
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
    K.judul("\n=== KATALOG LAGU ===")
    if len(katalog) == 0:
        K.kosong("Katalog masih kosong.")
    else:
        tabel = PrettyTable()
        tabel.field_names = ["ID", "Judul", "Penyanyi", "Genre"]
        for id_lagu in katalog:
            tabel.add_row([id_lagu, katalog[id_lagu]["judul"], katalog[id_lagu]["penyanyi"], katalog[id_lagu]["genre"]])
        K.cetak_tabel(tabel)

def tampilkan_playlist_user():
    K.judul("\n=== PLAYLIST SAYA ===")

    username = storage.username_aktif

    if username not in playlist or len(playlist[username]) == 0:
        K.kosong("Kamu belum membuat playlist.")
        return

    for nama_playlist in playlist[username]:
        K.daftar(f"\n=== PLAYLIST: {nama_playlist} ===")

        daftar_lagu = playlist[username][nama_playlist]

        if len(daftar_lagu) == 0:
            K.kosong("Playlist Anda belum ada lagu.")
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
                K.cetak_tabel(tabel)
            else:
                K.kosong("Tidak ada lagu yang tersedia di katalog.")
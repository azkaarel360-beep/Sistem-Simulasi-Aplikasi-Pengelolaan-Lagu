import time
import inquirer
import storage
from prettytable import PrettyTable
from storage import playlist, katalog, lagu_favorit
from read import tampilkan_katalog, tampilkan_playlist_user
from admin import cari_id_lagu
import os

def cari_nama_playlist(nama_input):
    """Cari nama playlist milik user aktif (tidak peka huruf besar/kecil)."""
    for nama in playlist[storage.username_aktif]:
        if nama.lower() == nama_input.strip().lower():
            return nama
    return ""

def cari_id_lagu(id_input):
    id_input = id_input.strip()

    if id_input.isdigit() and int(id_input) in katalog:
        return int(id_input)
    
    return None

def tampilkan_lagu_playlist(nama_playlist):
    daftar_lagu = playlist[storage.username_aktif][nama_playlist]

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
    if len(tabel.rows) == 0:
        print("\nPlaylist ini belum memiliki lagu!")
    else:
        print(f"\n=== PLAYLIST: {nama_playlist} ===")
        print(tabel)

def tampilkan_lagu_favorit():
    daftar_favorit = lagu_favorit[storage.username_aktif]
    print("\n=== DAFTAR LAGU FAVORIT ===")

    tabel = PrettyTable()
    tabel.field_names =   ["ID", "Judul", "Penyanyi", "Genre"]

    for id_lagu in daftar_favorit:
        if id_lagu in katalog:
            data = katalog[id_lagu]
            tabel.add_row([
                id_lagu,
                data["judul"],
                data["penyanyi"],
                data["genre"]
            ])

    if len(tabel.rows) == 0:
        print("Belum ada lagu favorit.")
    else:
        print(tabel)

def menu_favorit():
    while True:
        os.system("cls" if os.name == "nt" else "clear")

        pertanyaan = [
            inquirer.List(
                "menu",
                message="=== MENU LAGU FAVORIT ===",
                choices=[
                    "1. Tambah lagu favorit",
                    "2. Lihat lagu favorit",
                    "3. Hapus lagu favorit",
                    "4. Kembali"
                ]
            )
        ]

        jawaban = inquirer.prompt(pertanyaan)

        if jawaban is None:
            break

        menu = jawaban["menu"]

        if menu == "1. Tambah lagu favorit":
            if len(playlist[storage.username_aktif]) == 0:
                print("\nKamu belum memiliki playlist.")
            else:
                print("\n=== PILIH PLAYLIST ===")

                for nama_playlist in playlist[storage.username_aktif]:
                    print("-", nama_playlist)

                nama_asli = cari_nama_playlist(
                    input("\nNama playlist sumber: ")
                )

                if nama_asli == "":
                    print("\nPlaylist tidak ditemukan.")
                else:
                    tampilkan_lagu_playlist(nama_asli)

                    id_lagu = cari_id_lagu(
                        input("\nID lagu yang ingin dijadikan favorit: ")
                    )

                    if id_lagu is None:
                        print("\nID lagu tidak ditemukan di katalog.")
                    elif id_lagu not in playlist[storage.username_aktif][nama_asli]:
                        print("\nLagu tersebut tidak ada di playlist yang dipilih.")
                    elif id_lagu in lagu_favorit[storage.username_aktif]:
                        print("\nLagu sudah ada di daftar favorit.")
                    else:
                        lagu_favorit[storage.username_aktif][id_lagu] = True
                        print("\nLagu berhasil ditambahkan ke favorit.")

            input("\nEnter untuk kembali...")

        elif menu == "2. Lihat lagu favorit":
            tampilkan_lagu_favorit()
            input("\nEnter untuk kembali...")

        elif menu == "3. Hapus lagu favorit":
            tampilkan_lagu_favorit()

            if len(lagu_favorit[storage.username_aktif]) > 0:
                id_hapus = input("\nID lagu favorit yang ingin dihapus: ").strip()

                if id_hapus.isdigit() and int(id_hapus) in lagu_favorit[storage.username_aktif]:
                    del lagu_favorit[storage.username_aktif][int(id_hapus)]
                    print("\nLagu berhasil dihapus dari favorit.")
                else:
                    print("\nID lagu tidak ditemukan di daftar favorit.")

            input("\nEnter untuk kembali...")

        elif menu == "4. Kembali":
            break

# ==========================
def menu_user():
    if storage.username_aktif not in playlist:
        playlist[storage.username_aktif] = {}

    if storage.username_aktif not in playlist:
        playlist[storage.username_aktif] = {}
    
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        pertanyaan = [
            inquirer.List(
                "menu",
                message="=== MENU USER ===",
                choices=[
                    "1. Buat playlist",
                    "2. Lihat playlist",
                    "3. Tambah lagu ke playlist",
                    "4. Hapus lagu dari playlist",
                    "5. Lagu favorit",
                    "6. Logout"
                ]
            )
        ]

        jawaban = inquirer.prompt(pertanyaan)
        if jawaban is None:
            break
        menu = jawaban["menu"]

        if menu == "1. Buat playlist":
            nama_playlist = input("\nNama playlist Anda: ").strip()

            if nama_playlist == "":
                print("\nNama playlist tidak boleh kosong.")
            elif cari_nama_playlist(nama_playlist) != "":
                print("\nNama playlist itu sudah ada.")
            else:
                playlist[storage.username_aktif][nama_playlist] = {}
                print("\nPlaylist berhasil dibuat!")

            input("Enter untuk kembali...")

        elif menu == "2. Lihat playlist":
            tampilkan_playlist_user()
            input("\nEnter untuk kembali...")

        elif menu == "3. Tambah lagu ke playlist":
            print("\n=== PILIH PLAYLIST ===")

            for nama_playlist in playlist[storage.username_aktif]:
                print("-", nama_playlist)

            nama_asli = cari_nama_playlist(input("\nNama playlist tujuan: "))

            if nama_asli == "":
                print("\nPlaylist tidak ditemukan.")
            else:
                tampilkan_katalog()
                id_lagu = cari_id_lagu(input("\nID lagu yang ingin ditambahkan: "))

                if id_lagu is None:
                    print("\nID lagu tidak ditemukan.")
                elif id_lagu in playlist[storage.username_aktif][nama_asli]:
                    print("\nLagu sudah ada di playlist.")
                else:
                    playlist[storage.username_aktif][nama_asli][id_lagu] = True
                    print("\nLagu berhasil ditambahkan.")

            input("Enter untuk kembali...")

        
        elif menu == "4. Hapus lagu dari playlist":
            if len(playlist[storage.username_aktif]) == 0:
                print("\nKamu belum membuat playlist.")
            else:
                print("\n=== PILIH PLAYLIST ===")

                for nama_playlist in playlist[storage.username_aktif]:
                    print("-", nama_playlist)

                nama_asli = cari_nama_playlist(
                    input("\nNama playlist tujuan: ")
                )

                if nama_asli == "":
                    print("\nPlaylist tidak ditemukan.")
                else:
                    daftar_lagu = playlist[storage.username_aktif][nama_asli]

                    print(f"\n=== PLAYLIST: {nama_asli} ===")

                    if len(daftar_lagu) == 0:
                        print("Playlist ini belum memiliki lagu.")
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

                        print(tabel)

                        id_hapus = input("\nID lagu yang ingin dihapus: ").strip()

                        if id_hapus.isdigit() and int(id_hapus) in daftar_lagu:
                            del daftar_lagu[int(id_hapus)]
                            print("\nLagu berhasil dihapus dari playlist.")
                        else:
                            print("\nID lagu tidak ditemukan di playlist.")

            input("\nEnter untuk kembali...")
        elif menu == "5. Lagu favorit":
            menu_favorit()

        elif menu == "6. Logout":
            storage.username_aktif = ""
            print("\nTerima kasih dan sampai jumpa!")
            time.sleep(3)
            break
        else:
            print("Pilihan tidak tersedia.")
            input("Enter untuk kembali...")
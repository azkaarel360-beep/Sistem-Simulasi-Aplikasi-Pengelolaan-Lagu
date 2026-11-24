import time
import inquirer
from inquirer.themes import GreenPassion
import storage
import KOLOR as K
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
        K.kosong("\nPlaylist ini belum memiliki lagu!")
    else:
        K.judul(f"\n=== PLAYLIST: {nama_playlist} ===")
        K.cetak_tabel(tabel)

def tampilkan_lagu_favorit():
    daftar_favorit = lagu_favorit[storage.username_aktif]
    K.judul("\n=== DAFTAR LAGU FAVORIT ===")

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
        K.kosong("Belum ada lagu favorit.")
    else:
        K.cetak_tabel(tabel)

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

        jawaban = inquirer.prompt(pertanyaan, theme=GreenPassion())

        if jawaban is None:
            break

        menu = jawaban["menu"]

        if menu == "1. Tambah lagu favorit":
            if len(playlist[storage.username_aktif]) == 0:
                K.kosong("\nKamu belum memiliki playlist.")
            else:
                K.judul("\n=== PILIH PLAYLIST ===")

                for nama_playlist in playlist[storage.username_aktif]:
                    K.daftar("- " + nama_playlist)

                nama_asli = cari_nama_playlist(
                    K.tanya_yellow("\nNama playlist sumber: ")
                )

                if nama_asli == "":
                    K.gagal("\nPlaylist tidak ditemukan.")
                else:
                    tampilkan_lagu_playlist(nama_asli)

                    id_lagu = cari_id_lagu(
                        K.tanya_cyan("\nID lagu yang ingin dijadikan favorit: ")
                    )

                    if id_lagu is None:
                        K.gagal("\nID lagu tidak ditemukan di katalog.")
                    elif id_lagu not in playlist[storage.username_aktif][nama_asli]:
                        K.gagal("\nLagu tersebut tidak ada di playlist yang dipilih.")
                    elif id_lagu in lagu_favorit[storage.username_aktif]:
                        K.peringatan("\nLagu sudah ada di daftar favorit.")
                    else:
                        lagu_favorit[storage.username_aktif][id_lagu] = True
                        K.sukses("\nLagu berhasil ditambahkan ke favorit.")

            K.tanya_putih("\nEnter untuk kembali...")

        elif menu == "2. Lihat lagu favorit":
            tampilkan_lagu_favorit()
            K.tanya_putih("\nEnter untuk kembali...")

        elif menu == "3. Hapus lagu favorit":
            tampilkan_lagu_favorit()

            if len(lagu_favorit[storage.username_aktif]) > 0:
                id_hapus = K.tanya_merah("\nID lagu favorit yang ingin dihapus: ").strip()

                if id_hapus.isdigit() and int(id_hapus) in lagu_favorit[storage.username_aktif]:
                    del lagu_favorit[storage.username_aktif][int(id_hapus)]
                    K.sukses("\nLagu berhasil dihapus dari favorit.")
                else:
                    K.gagal("\nID lagu tidak ditemukan di daftar favorit.")

            K.tanya_putih("\nEnter untuk kembali...")

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

        jawaban = inquirer.prompt(pertanyaan, theme=GreenPassion())
        if jawaban is None:
            break
        menu = jawaban["menu"]

        if menu == "1. Buat playlist":
            nama_playlist = K.tanya_magenta("\nNama playlist Anda: ").strip()

            if nama_playlist == "":
                K.gagal("\nNama playlist tidak boleh kosong.")
            elif cari_nama_playlist(nama_playlist) != "":
                K.gagal("\nNama playlist itu sudah ada.")
            else:
                playlist[storage.username_aktif][nama_playlist] = {}
                K.sukses("\nPlaylist berhasil dibuat!")

            K.tanya_putih("Enter untuk kembali...")

        elif menu == "2. Lihat playlist":
            tampilkan_playlist_user()
            K.tanya_putih("\nEnter untuk kembali...")

        elif menu == "3. Tambah lagu ke playlist":
            K.judul("\n=== PILIH PLAYLIST ===")

            for nama_playlist in playlist[storage.username_aktif]:
                K.daftar("- " + nama_playlist)

            nama_asli = cari_nama_playlist(K.tanya_yellow("\nNama playlist tujuan: "))

            if nama_asli == "":
                K.gagal("\nPlaylist tidak ditemukan.")
            else:
                tampilkan_katalog()
                id_lagu = cari_id_lagu(K.tanya_hijau("\nID lagu yang ingin ditambahkan: "))

                if id_lagu is None:
                    K.gagal("\nID lagu tidak ditemukan.")
                elif id_lagu in playlist[storage.username_aktif][nama_asli]:
                    K.peringatan("\nLagu sudah ada di playlist.")
                else:
                    playlist[storage.username_aktif][nama_asli][id_lagu] = True
                    K.sukses("\nLagu berhasil ditambahkan.")

            K.tanya_putih("Enter untuk kembali...")

        
        elif menu == "4. Hapus lagu dari playlist":
            if len(playlist[storage.username_aktif]) == 0:
                K.kosong("\nKamu belum membuat playlist.")
            else:
                K.judul("\n=== PILIH PLAYLIST ===")

                for nama_playlist in playlist[storage.username_aktif]:
                    K.daftar("- " + nama_playlist)

                nama_asli = cari_nama_playlist(
                    K.tanya_yellow("\nNama playlist tujuan: ")
                )

                if nama_asli == "":
                    K.gagal("\nPlaylist tidak ditemukan.")
                else:
                    daftar_lagu = playlist[storage.username_aktif][nama_asli]

                    K.judul(f"\n=== PLAYLIST: {nama_asli} ===")

                    if len(daftar_lagu) == 0:
                        K.kosong("Playlist ini belum memiliki lagu.")
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

                        K.cetak_tabel(tabel)

                        id_hapus = K.tanya_merah("\nID lagu yang ingin dihapus: ").strip()

                        if id_hapus.isdigit() and int(id_hapus) in daftar_lagu:
                            del daftar_lagu[int(id_hapus)]
                            K.sukses("\nLagu berhasil dihapus dari playlist.")
                        else:
                            K.gagal("\nID lagu tidak ditemukan di playlist.")

            K.tanya_putih("\nEnter untuk kembali...")
        elif menu == "5. Lagu favorit":
            menu_favorit()

        elif menu == "6. Logout":
            storage.username_aktif = ""
            K.sukses("\nTerima kasih dan sampai jumpa!")
            time.sleep(3)
            break
        else:
            K.gagal("Pilihan tidak tersedia.")
            K.tanya_putih("Enter untuk kembali...")
import time
import inquirer
import storage
from storage import playlist, katalog
from read import tampilkan_katalog, tampilkan_playlist_user
from admin import cari_id_lagu
import os

def cari_nama_playlist(nama_input):
    """Cari nama playlist milik user aktif (tidak peka huruf besar/kecil)."""
    for nama in playlist[storage.username_aktif]:
        if nama.lower() == nama_input.strip().lower():
            return nama
    return ""

def menu_user():
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
                    "5. Logout"
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
            print("\n=== PILIH PLAYLIST ===")
            for nama_playlist in playlist[storage.username_aktif]:
                print("-", nama_playlist)
            nama_asli = cari_nama_playlist(input("\nNama playlist tujuan: "))

            if nama_asli == "":
                print("\nPlaylist tidak ditemukan.")
            else:
                print("\nLagu di playlist", nama_asli)
                for id_lagu in playlist[storage.username_aktif][nama_asli]:
                    if id_lagu in katalog:
                        data = katalog[id_lagu]
                        print(id_lagu, "-", data["judul"], "-", data["penyanyi"], "-", data["genre"])

                id_hapus = input("\nID lagu yang ingin dihapus: ").strip()
                if id_hapus.isdigit() and int(id_hapus) in playlist[storage.username_aktif][nama_asli]:
                    del playlist[storage.username_aktif][nama_asli][int(id_hapus)]
                    print("\nLagu telah dihapus dari playlist.")
                else:
                    print("\nID lagu tidak ada di playlist.")
            input("Enter untuk kembali...")

        elif menu == "5. Logout":
            storage.username_aktif = ""
            print("\nTerima kasih dan sampai jumpa!.")
            time.sleep(3)
            break
        else:
            print("Pilihan tidak tersedia.")
            input("Enter untuk kembali...")
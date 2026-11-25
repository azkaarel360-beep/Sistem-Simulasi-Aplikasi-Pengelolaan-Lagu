import time
import inquirer
from inquirer.themes import GreenPassion
from colorama import Fore, Style
import storage
from prettytable import PrettyTable
from storage import playlist, katalog, lagu_favorit
from read import tampilkan_katalog, tampilkan_playlist_user
from admin import cari_id_lagu, ubah_ke_angka, IDTidakValid
import os

def playlist_saya():
    return playlist.setdefault(storage.username_aktif, {})

def favorit_saya():
    return lagu_favorit.setdefault(storage.username_aktif, {})

def cari_nama_playlist(nama_input):
    for nama in playlist_saya():
        if nama.lower() == nama_input.strip().lower():
            return nama
    return ""

def buat_tabel_lagu(daftar_id):
    tabel = PrettyTable()
    tabel.field_names = ["ID", "Judul", "Penyanyi", "Genre"]
    for id_lagu in daftar_id:
        if id_lagu in katalog:
            data = katalog[id_lagu]
            tabel.add_row([id_lagu, data["judul"], data["penyanyi"], data["genre"]])
    return tabel

def tampilkan_lagu_playlist(nama_playlist):
    tabel = buat_tabel_lagu(playlist_saya()[nama_playlist])

    if len(tabel.rows) == 0:
        print(Style.DIM + "\nPlaylist ini belum memiliki lagu!")
    else:
        print(Fore.CYAN + f"\n=== PLAYLIST: {nama_playlist} ===")
        print(Fore.LIGHTCYAN_EX + str(tabel))

def tampilkan_lagu_favorit():
    print(Fore.CYAN + "\n=== DAFTAR LAGU FAVORIT ===")
    tabel = buat_tabel_lagu(favorit_saya())
    if len(tabel.rows) == 0:
        print(Style.DIM + "Belum ada lagu favorit.")
    else:
        print(Fore.LIGHTCYAN_EX + str(tabel))

def pilih_playlist(pesan):
    print(Fore.CYAN + "\n=== PILIH PLAYLIST ===")
    for nama_playlist in playlist_saya():
        print(Fore.MAGENTA + "- " + nama_playlist)
    print(Fore.YELLOW + pesan, end="")
    return cari_nama_playlist(input())

def menu_kelola_playlist():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        pertanyaan = [
            inquirer.List(
                "menu",
                message="=== MENU KELOLA PLAYLIST ===",
                choices=[
                    "1. Ganti nama playlist",
                    "2. Hapus playlist",
                    "3. Tambah lagu ke playlist",
                    "4. Hapus lagu dari playlist",
                    "5. Kembali"
                ]
            )
        ]
        jawaban = inquirer.prompt(pertanyaan, theme=GreenPassion())
        if jawaban is None:
            break
        menu = jawaban["menu"]

        try:
            if menu == "1. Ganti nama playlist":
                if len(playlist_saya()) == 0:
                    print(Style.DIM + "\nKamu belum membuat playlist.")
                else:
                    nama_asli = pilih_playlist("\nNama playlist yang ingin diganti: ")

                    if nama_asli == "":
                        print(Fore.RED + "\n✘ Playlist tidak ditemukan.")
                    else:
                        print(Fore.CYAN + "\nNama playlist baru: ", end="")
                        nama_baru = input().strip()

                        if nama_baru == "":
                            print(Fore.RED + "\n✘ Nama playlist tidak boleh kosong.")
                        elif cari_nama_playlist(nama_baru) != "":
                            print(Fore.RED + "\n✘ Nama playlist itu sudah ada.")
                        else:
                            playlist_saya()[nama_baru] = playlist_saya().pop(nama_asli)
                            print(Fore.GREEN + "\n✔ Nama playlist berhasil diganti!")
            
            elif menu == "2. Hapus playlist":
                if len(playlist_saya()) == 0:
                    print(Style.DIM + "\nKamu belum membuat playlist.")
                else:
                    nama_asli = pilih_playlist("\nNama playlist yang ingin dihapus: ")

                    if nama_asli == "":
                        print(Fore.RED + "\n✘ Playlist tidak ditemukan.")
                    else:
                        del playlist_saya()[nama_asli]
                        print(Fore.GREEN + "\n✔ Playlist berhasil dihapus!")

            elif menu == "3. Tambah lagu ke playlist":
                if len(playlist_saya()) == 0:
                    print(Style.DIM + "\nKamu belum membuat playlist.")
                elif len(katalog) == 0:
                    print(Style.DIM + "\nKatalog masih kosong, belum ada lagu yang bisa ditambahkan.")
                else:
                    nama_asli = pilih_playlist("\nNama playlist tujuan: ")
            
                    if nama_asli == "":
                        print(Fore.RED + "\n✘ Playlist tidak ditemukan.")
                    else:
                        tampilkan_katalog()
            
                        try:
                            print(Fore.GREEN + "\nID lagu yang ingin ditambahkan: ", end="")
                            id_lagu = cari_id_lagu(input())
                        except IDTidakValid as pesan_error:
                            print(Fore.RED + f"\n✘ {pesan_error}")
                        else:
                            if id_lagu in playlist_saya()[nama_asli]:
                                print(Fore.YELLOW + "\n⚠ Lagu sudah ada di playlist.")
                            else:
                                playlist_saya()[nama_asli][id_lagu] = True
                                print(Fore.GREEN + "\n✔ Lagu berhasil ditambahkan.")

            elif menu == "4. Hapus lagu dari playlist":
                if len(playlist_saya()) == 0:
                    print(Style.DIM + "\nKamu belum membuat playlist.")
                else:
                    nama_asli = pilih_playlist("\nNama playlist tujuan: ")
            
                    if nama_asli == "":
                        print(Fore.RED + "\n✘ Playlist tidak ditemukan.")
                    else:
                        daftar_lagu = playlist_saya()[nama_asli]
                        print(Fore.CYAN + f"\n=== PLAYLIST: {nama_asli} ===")
            
                        if len(daftar_lagu) == 0:
                            print(Style.DIM + "Playlist ini belum memiliki lagu.")
                        else:
                            print(Fore.LIGHTCYAN_EX + str(buat_tabel_lagu(daftar_lagu)))
            
                            try:
                                print(Fore.RED + "\nID lagu yang ingin dihapus: ", end="")
                                id_hapus = ubah_ke_angka(input())
                                del daftar_lagu[id_hapus]
                            except IDTidakValid as pesan_error:
                                print(Fore.RED + f"\n✘ {pesan_error}")
                            except KeyError:
                                print(Fore.RED + "\n✘ ID lagu tidak ditemukan di playlist.")
                            else:
                                print(Fore.GREEN + "\n✔ Lagu berhasil dihapus dari playlist.")

            elif menu == "5. Kembali":
                break

        except Exception as pesan_error:
            print(Fore.RED + f"\n✘ Terjadi kesalahan: {pesan_error}")
        finally:
            if menu != "5. Kembali":
                print(Fore.WHITE + "\nEnter untuk kembali...", end="")
                input()

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

        try:
            if menu == "1. Tambah lagu favorit":
                if len(playlist_saya()) == 0:
                    print(Style.DIM + "\nKamu belum memiliki playlist.")
                elif not any(len(isi) > 0 for isi in playlist_saya().values()):
                    print(Style.DIM + "\nSemua playlist kamu masih kosong, belum ada lagu yang bisa dijadikan favorit.")
                else:
                    nama_asli = pilih_playlist("\nNama playlist sumber: ")

                    if nama_asli == "":
                        print(Fore.RED + "\n✘ Playlist tidak ditemukan.")
                    elif len(playlist_saya()[nama_asli]) == 0:
                        print(Style.DIM + "\nPlaylist ini belum memiliki lagu!")
                    else:
                        tampilkan_lagu_playlist(nama_asli)

                        try:
                            print(Fore.CYAN + "\nID lagu yang ingin dijadikan favorit: ", end="")
                            id_lagu = cari_id_lagu(input())
                        except IDTidakValid as pesan_error:
                            print(Fore.RED + f"\n✘ {pesan_error}")
                        else:
                            if id_lagu not in playlist_saya()[nama_asli]:
                                print(Fore.RED + "\n✘ Lagu tersebut tidak ada di playlist yang dipilih.")
                            elif id_lagu in favorit_saya():
                                print(Fore.YELLOW + "\n⚠ Lagu sudah ada di daftar favorit.")
                            else:
                                favorit_saya()[id_lagu] = True
                                print(Fore.GREEN + "\n✔ Lagu berhasil ditambahkan ke favorit.")

            elif menu == "2. Lihat lagu favorit":
                tampilkan_lagu_favorit()

            elif menu == "3. Hapus lagu favorit":
                tampilkan_lagu_favorit()

                if len(favorit_saya()) > 0:
                    try:
                        print(Fore.RED + "\nID lagu favorit yang ingin dihapus: ", end="")
                        id_hapus = ubah_ke_angka(input())
                        del favorit_saya()[id_hapus]
                    except IDTidakValid as pesan_error:
                        print(Fore.RED + f"\n✘ {pesan_error}")
                    except KeyError:
                        print(Fore.RED + "\n✘ ID lagu tidak ditemukan di daftar favorit.")
                    else:
                        print(Fore.GREEN + "\n✔ Lagu berhasil dihapus dari favorit.")

            elif menu == "4. Kembali":
                break

        except Exception as pesan_error:
            print(Fore.RED + f"\n✘ Terjadi kesalahan: {pesan_error}")
        finally:
            if menu != "4. Kembali":
                print(Fore.WHITE + "\nEnter untuk kembali...", end="")
                input()

def menu_user():
    playlist_saya()
    favorit_saya()

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        pertanyaan = [
            inquirer.List(
                "menu",
                message="=== MENU USER ===",
                choices=[
                    "1. Buat playlist",
                    "2. Lihat playlist",
                    "3. Kelola playlist",
                    "4. Lagu favorit",
                    "5. Logout"
                ]
            )
        ]

        jawaban = inquirer.prompt(pertanyaan, theme=GreenPassion())
        if jawaban is None:
            break
        menu = jawaban["menu"]

        try:
            if menu == "1. Buat playlist":
                print(Fore.MAGENTA + "\nNama playlist Anda: ", end="")
                nama_playlist = input().strip()

                if nama_playlist == "":
                    print(Fore.RED + "\n✘ Nama playlist tidak boleh kosong.")
                elif cari_nama_playlist(nama_playlist) != "":
                    print(Fore.RED + "\n✘ Nama playlist itu sudah ada.")
                else:
                    playlist_saya()[nama_playlist] = {}
                    print(Fore.GREEN + "\n✔ Playlist berhasil dibuat!")

            elif menu == "2. Lihat playlist":
                if len(playlist_saya()) == 0:
                    print(Style.DIM + "\nKamu belum membuat playlist.")
                else:
                    nama_asli = pilih_playlist("\nNama playlist tujuan: ")
                
                    if nama_asli == "":
                        print(Fore.RED + "\n✘ Playlist tidak ditemukan.")
                    else:
                        tampilkan_playlist_user(nama_asli)

            elif menu == "3. Kelola playlist":
                menu_kelola_playlist()
                continue

            elif menu == "4. Lagu favorit":
                menu_favorit()
                continue

            elif menu == "5. Logout":
                storage.username_aktif = ""
                print(Fore.GREEN + "\n✔ Terima kasih dan sampai jumpa!")
                time.sleep(3)
                break

            else:
                print(Fore.RED + "✘ Pilihan tidak tersedia.")

        except Exception as pesan_error:
            print(Fore.RED + f"\n✘ Terjadi kesalahan: {pesan_error}")
        finally:
            if menu not in ("5. Lagu favorit", "6. Logout"):
                print(Fore.WHITE + "\nEnter untuk kembali...", end="")
                input()
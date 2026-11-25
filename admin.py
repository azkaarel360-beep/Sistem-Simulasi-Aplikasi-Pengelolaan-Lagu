import time
import inquirer
from inquirer.themes import RedSolace
from colorama import Fore
import storage
from storage import playlist, katalog, lagu_favorit, username_admin
from read import tampilkan_katalog
import os

class IDTidakValid(Exception):
    pass

def ubah_ke_angka(teks):
    try:
        return int(teks.strip())
    except ValueError:
        raise IDTidakValid("ID harus berupa angka.")


def cari_id_lagu(teks):
    id_lagu = ubah_ke_angka(teks)
    if id_lagu not in katalog:
        raise IDTidakValid("ID lagu tidak ditemukan.")
    return id_lagu


def lagu_kembar(judul, penyanyi, genre, abaikan_id=None):
    for id_lagu in katalog:
        if id_lagu == abaikan_id:
            continue
        data = katalog[id_lagu]
        if (data["judul"].lower() == judul.lower()
                and data["penyanyi"].lower() == penyanyi.lower()
                and data["genre"].lower() == genre.lower()):
            return True
    return False


def tambah_lagu_katalog():
    print(Fore.CYAN + "\nJudul lagu: ", end="")
    judul = input().strip()
    print(Fore.MAGENTA + "Penyanyi: ", end="")
    penyanyi = input().strip()
    print(Fore.GREEN + "Genre: ", end="")
    genre = input().strip()

    if judul == "" or penyanyi == "" or genre == "":
        print(Fore.RED + "\n✘ Input tidak boleh kosong.")
    elif lagu_kembar(judul, penyanyi, genre):
        print(Fore.RED + "\n✘ Lagu dengan judul, penyanyi, dan genre yang sama sudah ada di katalog.")
    else:
        id_baru = storage.id_berikutnya
        katalog[id_baru] = {"judul": judul, "penyanyi": penyanyi, "genre": genre}
        storage.id_berikutnya += 1
        print(Fore.GREEN + f"\n✔ Lagu berhasil ditambahkan dengan ID {id_baru}.")

def ubah_lagu_katalog():
    tampilkan_katalog()
    if len(katalog) == 0:
        return

    try:
        print(Fore.YELLOW + "\nMasukkan ID lagu yang ingin diubah: ", end="")
        id_lagu = cari_id_lagu(input())
    except IDTidakValid as pesan_error:
        print(Fore.RED + f"\n✘ {pesan_error}")
        return

    data = katalog[id_lagu]
    print(Fore.BLUE + "\nℹ Kosongkan bagian jika tidak ingin mengubahnya.")
    print(Fore.CYAN + f"Judul baru untuk {data['judul']}: ", end="")
    judul_baru = input().strip()
    print(Fore.MAGENTA + f"Penyanyi baru untuk {data['penyanyi']}: ", end="")
    penyanyi_baru = input().strip()
    print(Fore.GREEN + f"Genre baru untuk {data['genre']}: ", end="")
    genre_baru = input().strip()

    if judul_baru == "" and penyanyi_baru == "" and genre_baru == "":
        print(Fore.BLUE + "\nℹ Tidak ada yang diperbarui.")
        return

    judul_akhir = judul_baru if judul_baru != "" else data["judul"]
    penyanyi_akhir = penyanyi_baru if penyanyi_baru != "" else data["penyanyi"]
    genre_akhir = genre_baru if genre_baru != "" else data["genre"]

    if lagu_kembar(judul_akhir, penyanyi_akhir, genre_akhir, abaikan_id=id_lagu):
        print(Fore.RED + "\n✘ Lagu dengan judul, penyanyi, dan genre yang sama sudah ada di katalog.")
    else:
        data["judul"] = judul_akhir
        data["penyanyi"] = penyanyi_akhir
        data["genre"] = genre_akhir
        print(Fore.GREEN + "\n✔ Data lagu berhasil diperbarui.")


def hapus_lagu_katalog():
    tampilkan_katalog()
    if len(katalog) == 0:
        return

    try:
        print(Fore.RED + "\nMasukkan ID lagu yang ingin dihapus: ", end="")
        id_lagu = cari_id_lagu(input())
    except IDTidakValid as pesan_error:
        print(Fore.RED + f"\n✘ {pesan_error}")
        return

    del katalog[id_lagu]

    for data_user in playlist:
        for nama_playlist in playlist[data_user]:
            if id_lagu in playlist[data_user][nama_playlist]:
                del playlist[data_user][nama_playlist][id_lagu]

    for data_user in lagu_favorit:
        if id_lagu in lagu_favorit[data_user]:
            del lagu_favorit[data_user][id_lagu]

    print(Fore.GREEN + "\n✔ Lagu berhasil dihapus dari katalog.")


def menu_admin():
    if storage.username_aktif.lower() != username_admin.lower():
        return

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        pertanyaan = [
            inquirer.List(
                "menu",
                message="=== MENU ADMIN ===",
                choices=[
                    "1. Tambah lagu ke katalog",
                    "2. Lihat katalog",
                    "3. Update katalog lagu",
                    "4. Hapus lagu dari katalog",
                    "5. Logout"
                ]
            )
        ]
        jawaban = inquirer.prompt(pertanyaan, theme=RedSolace())
        if jawaban is None:
            break
        menu = jawaban["menu"]

        try:
            if menu == "1. Tambah lagu ke katalog":
                tambah_lagu_katalog()

            elif menu == "2. Lihat katalog":
                tampilkan_katalog()

            elif menu == "3. Update katalog lagu":
                ubah_lagu_katalog()

            elif menu == "4. Hapus lagu dari katalog":
                hapus_lagu_katalog()

            elif menu == "5. Logout":
                storage.username_aktif = ""
                print(Fore.GREEN + "\n✔ Terima kasih dan sampai jumpa!.")
                time.sleep(3)
                break

            else:
                print(Fore.RED + "\n✘ Pilihan tidak tersedia.")

        except Exception as pesan_error:
            print(Fore.RED + f"\n✘ Terjadi kesalahan: {pesan_error}")
        finally:
            if menu != "5. Logout":
                print(Fore.WHITE + "\nEnter untuk kembali...", end="")
                input()
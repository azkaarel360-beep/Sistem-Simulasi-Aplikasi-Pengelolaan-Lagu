import time
import inquirer
from inquirer.themes import RedSolace
import storage
import KOLOR as K
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
    judul = K.tanya_cyan("\nJudul lagu: ").strip()
    penyanyi = K.tanya_magenta("Penyanyi: ").strip()
    genre = K.tanya_hijau("Genre: ").strip()
    if judul == "" or penyanyi == "" or genre == "":
        K.gagal("\nInput tidak boleh kosong.")
    elif lagu_kembar(judul, penyanyi, genre):
        K.gagal("\nLagu dengan judul, penyanyi, dan genre yang sama sudah ada di katalog.")
    else:
        id_baru = storage.id_berikutnya
        katalog[id_baru] = {"judul": judul, "penyanyi": penyanyi, "genre": genre}
        storage.id_berikutnya += 1
        K.sukses(f"\nLagu berhasil ditambahkan dengan ID {id_baru}.")

def ubah_lagu_katalog():
    tampilkan_katalog()
    if len(katalog) == 0:
        return

    try:
        id_lagu = cari_id_lagu(K.tanya_yellow("\nMasukkan ID lagu yang ingin diubah: "))
    except IDTidakValid as pesan_error:
        K.gagal(f"\n{pesan_error}")
        return

    data = katalog[id_lagu]
    K.info("\nKosongkan bagian jika tidak ingin mengubahnya.")
    judul_baru = K.tanya_cyan(f"Judul baru untuk {data['judul']}: ").strip()
    penyanyi_baru = K.tanya_magenta(f"Penyanyi baru untuk {data['penyanyi']}: ").strip()
    genre_baru = K.tanya_hijau(f"Genre baru untuk {data['genre']}: ").strip()

    if judul_baru == "" and penyanyi_baru == "" and genre_baru == "":
        K.info("\nTidak ada yang diperbarui.")
        return

    judul_akhir = judul_baru if judul_baru != "" else data["judul"]
    penyanyi_akhir = penyanyi_baru if penyanyi_baru != "" else data["penyanyi"]
    genre_akhir = genre_baru if genre_baru != "" else data["genre"]

    if lagu_kembar(judul_akhir, penyanyi_akhir, genre_akhir, abaikan_id=id_lagu):
        K.gagal("\nLagu dengan judul, penyanyi, dan genre yang sama sudah ada di katalog.")
    else:
        data["judul"] = judul_akhir
        data["penyanyi"] = penyanyi_akhir
        data["genre"] = genre_akhir
        K.sukses("\nData lagu berhasil diperbarui.")


def hapus_lagu_katalog():
    tampilkan_katalog()
    if len(katalog) == 0:
        return

    try:
        id_lagu = cari_id_lagu(K.tanya_merah("\nMasukkan ID lagu yang ingin dihapus: "))
    except IDTidakValid as pesan_error:
        K.gagal(f"\n{pesan_error}")
        return

    del katalog[id_lagu]

    for data_user in playlist:
        for nama_playlist in playlist[data_user]:
            if id_lagu in playlist[data_user][nama_playlist]:
                del playlist[data_user][nama_playlist][id_lagu]

    for data_user in lagu_favorit:
        if id_lagu in lagu_favorit[data_user]:
            del lagu_favorit[data_user][id_lagu]

    K.sukses("\nLagu berhasil dihapus dari katalog.")


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
                K.sukses("\nTerima kasih dan sampai jumpa!.")
                time.sleep(3)
                break

            else:
                K.gagal("\nPilihan tidak tersedia.")

        except Exception as pesan_error:
            K.gagal(f"\nTerjadi kesalahan: {pesan_error}")
        finally:
            if menu != "5. Logout":
                K.tanya_putih("\nEnter untuk kembali...")
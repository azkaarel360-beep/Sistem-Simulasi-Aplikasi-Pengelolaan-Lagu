import time
import inquirer
import storage
from storage import playlist, katalog, username_admin
from read import tampilkan_katalog
import os

def cari_id_lagu(teks):
    """Ubah input menjadi ID lagu yang valid, atau None jika tidak ada."""
    teks = teks.strip()
    if teks.isdigit() and int(teks) in katalog:
        return int(teks)
    return None

def lagu_kembar(judul, penyanyi, genre, abaikan_id=None):
    """True jika sudah ada lagu dengan judul, penyanyi, DAN genre yang sama persis."""
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
    judul = input("\nJudul lagu: ").strip()
    penyanyi = input("Penyanyi: ").strip()
    genre = input("Genre: ").strip()
    if judul == "" or penyanyi == "" or genre == "":
        print("\nInput tidak boleh kosong.")
    elif lagu_kembar(judul, penyanyi, genre):
        print("\nLagu dengan judul, penyanyi, dan genre yang sama sudah ada di katalog.")
    else:
        id_baru = storage.id_berikutnya
        katalog[id_baru] = {"judul": judul, "penyanyi": penyanyi, "genre": genre}
        storage.id_berikutnya += 1
        print(f"\nLagu berhasil ditambahkan dengan ID {id_baru}.")

def ubah_lagu_katalog():
    tampilkan_katalog()
    if len(katalog) == 0:
        return
    id_lagu = cari_id_lagu(input("\nMasukkan ID lagu yang ingin diubah: "))
    if id_lagu is None:
        print("\nID lagu tidak ditemukan.")
        return

    data = katalog[id_lagu]
    print("\nKosongkan bagian jika tidak ingin mengubahnya.")
    judul_baru = input(f"Judul baru untuk {data['judul']}: ").strip()
    penyanyi_baru = input(f"Penyanyi baru untuk {data['penyanyi']}: ").strip()
    genre_baru = input(f"Genre baru untuk {data['genre']}: ").strip()

    if judul_baru == "" and penyanyi_baru == "" and genre_baru == "":
        print("\nTidak ada yang diperbarui.")
        return

    judul_akhir = judul_baru if judul_baru != "" else data["judul"]
    penyanyi_akhir = penyanyi_baru if penyanyi_baru != "" else data["penyanyi"]
    genre_akhir = genre_baru if genre_baru != "" else data["genre"]

    if lagu_kembar(judul_akhir, penyanyi_akhir, genre_akhir, abaikan_id=id_lagu):
        print("\nLagu dengan judul, penyanyi, dan genre yang sama sudah ada di katalog.")
    else:
        data["judul"] = judul_akhir
        data["penyanyi"] = penyanyi_akhir
        data["genre"] = genre_akhir
        print("\nData lagu berhasil diperbarui.")

def hapus_lagu_katalog():
    tampilkan_katalog()
    if len(katalog) == 0:
        return
    id_lagu = cari_id_lagu(input("\nMasukkan ID lagu yang ingin dihapus: ")).strip()
    if id_lagu is None:
        print("\nID lagu tidak ditemukan.")
        return

    del katalog[id_lagu]
    for data_user in playlist:
        for nama_playlist in playlist[data_user]:
            if id_lagu in playlist[data_user][nama_playlist]:
                del playlist[data_user][nama_playlist][id_lagu]
    print("\nLagu berhasil dihapus dari katalog.")

def menu_admin():
    if storage.username_aktif.lower() == username_admin.lower():
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
            jawaban = inquirer.prompt(pertanyaan)
            if jawaban is None:
                break
            menu = jawaban["menu"]

            if menu == "1. Tambah lagu ke katalog":
                tambah_lagu_katalog()
                input("\nEnter untuk kembali...")

            elif menu == "2. Lihat katalog":
                tampilkan_katalog()
                input("\nEnter untuk kembali...")

            elif menu == "3. Update katalog lagu":
                ubah_lagu_katalog()
                input("\nTekan Enter untuk kembali...")

            elif menu == "4. Hapus lagu dari katalog":
                hapus_lagu_katalog()
                input("\nEnter untuk kembali...")

            elif menu == "5. Logout":
                storage.username_aktif = ""
                print("\nTerima kasih dan sampai jumpa!.")
                time.sleep(3)
                break
            else:
                print("\nPilihan tidak tersedia.")
                input("Enter untuk kembali...")
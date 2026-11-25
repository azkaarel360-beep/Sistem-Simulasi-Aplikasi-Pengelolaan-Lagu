import storage
from colorama import Fore


def cari_akun(username, password):
    for nama_akun in storage.akun:
        if username.lower() == nama_akun.lower() and password == storage.akun[nama_akun]:
            return nama_akun
    raise ValueError("Username atau password salah.")


def autentikasi_login():
    storage.username_aktif = ""

    for percobaan in range(1, 4):
        try:
            print(Fore.BLUE + "\nSilahkan masukkan username: ", end="")
            username = input().strip()
            print(Fore.MAGENTA + "Silahkan masukkan password: ", end="")
            password = input().strip()

            if username == "" or password == "":
                raise ValueError("Username dan password tidak boleh kosong.")

            nama_login = cari_akun(username, password)

        except ValueError as pesan_error:
            print(Fore.RED + f"\n✘ {pesan_error}")
            sisa_percobaan = 3 - percobaan

            if sisa_percobaan == 0:
                print(Fore.RED + "\n✘ Kesempatan login habis.")
            else:
                print(Fore.YELLOW + f"\n⚠ Sisa percobaan: {sisa_percobaan}")

            print(Fore.WHITE + "Enter untuk kembali...", end="")
            input()
        else:
            storage.username_aktif = nama_login
            return nama_login

    return ""
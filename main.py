import time
import storage

from colorama import init, Fore
from create import buat_akun_baru
from login import autentikasi_login
from admin import menu_admin
from user import menu_user
from read import tampilkan_menu_awal

init(autoreset=True)

try:
    while True:
        pilihan = tampilkan_menu_awal()

        if pilihan == "1":
            username_aktif = autentikasi_login()

            if username_aktif != "":
                if username_aktif.lower() == storage.username_admin.lower():
                    menu_admin()
                else:
                    menu_user()

        elif pilihan == "2":
            buat_akun_baru()

        elif pilihan == "3":
            print(Fore.GREEN + "\n✔ Terima kasih dan sampai jumpa")
            time.sleep(3)
            break

except KeyboardInterrupt:
    print(Fore.BLUE + "\nℹ Program dihentikan.")
    print(Fore.GREEN + "✔ Terimakasih dan sampai jumpa!")
except EOFError:
    print(Fore.RED + "\n✘ Input terputus. Program dihentikan.")
except Exception as pesan_error:
    print(Fore.RED + f"\n✘ Terjadi kesalahan tak terduga: {pesan_error}")
finally:
    storage.username_aktif = ""
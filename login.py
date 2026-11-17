import storage

percobaan = 3

def autentikasi_login():
    for i in range(1, percobaan + 1):
        username = input("\nSilahkan masukkan username: ").strip()
        password = input("Silahkan masukkan password: ").strip()

        nama_login = ""
        for nama_akun in storage.akun:
            if username.lower() == nama_akun.lower() and password == storage.akun[nama_akun]:
                nama_login = nama_akun
                break

        if nama_login != "":
            storage.username_aktif = nama_login
            return storage.username_aktif

        sisa = percobaan - i
        if sisa > 0:
            print(f"\nUsername atau password salah. Sisa percobaan: {sisa}")
        else:
            print("\nUsername atau password salah.")

    print("\nPercobaan login habis (3 kali). Kembali ke menu utama.")
    input("Enter untuk kembali...")
    return ""
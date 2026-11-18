import storage

def autentikasi_login():
    for i in range(1,4):
        username = input("\nSilahkan masukkan username: ")
        password = input("Silahkan masukkan password: ")
        nama_login = ""
    
        for nama_akun in storage.akun:
            if username.lower() == nama_akun.lower() and password == storage.akun[nama_akun]:
                nama_login = nama_akun
                break
        
        if nama_login != "":
            storage.username_aktif = nama_login
            return storage.username_aktif
        else:
            sisa_percobaan = 3 - i
            print("\nUsername atau password salah.")
            if sisa_percobaan == 0:
                print("\nKesempatan login habis. Program dihentikan.")
                break

            print(f"Sisa percobaan: {sisa_percobaan}")
            input("Enter untuk kembali...")
        
        storage.username_aktif = nama_login
        return storage.username_aktif
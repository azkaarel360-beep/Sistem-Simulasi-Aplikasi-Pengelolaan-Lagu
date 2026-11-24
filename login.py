import storage
import KOLOR as K

def autentikasi_login():
    for i in range(1,4):
        username = K.tanya_biru("\nSilahkan masukkan username: ").strip()
        password = K.tanya_magenta("Silahkan masukkan password: ").strip()
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
            K.gagal("\nUsername atau password salah.")
            if sisa_percobaan == 0:
                K.gagal("\nKesempatan login habis. Program dihentikan.")
                break

            K.peringatan(f"\nSisa percobaan: {sisa_percobaan}")
            K.tanya_putih("Enter untuk kembali...")
        
    storage.username_aktif = nama_login
    return storage.username_aktif
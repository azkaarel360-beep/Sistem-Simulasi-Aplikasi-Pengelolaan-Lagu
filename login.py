import storage
import KOLOR as K


def cari_akun(username, password):
    for nama_akun in storage.akun:
        if username.lower() == nama_akun.lower() and password == storage.akun[nama_akun]:
            return nama_akun
    raise ValueError("Username atau password salah.")


def autentikasi_login():
    storage.username_aktif = ""

    for percobaan in range(1, 4):
        try:
            username = K.tanya_biru("\nSilahkan masukkan username: ").strip()
            password = K.tanya_magenta("Silahkan masukkan password: ").strip()

            if username == "" or password == "":
                raise ValueError("Username dan password tidak boleh kosong.")

            nama_login = cari_akun(username, password)

        except ValueError as pesan_error:
            K.gagal(f"\n{pesan_error}")
            sisa_percobaan = 3 - percobaan

            if sisa_percobaan == 0:
                K.gagal("\nKesempatan login habis.")
                K.tanya_putih("Enter untuk kembali...")
            else:
                K.peringatan(f"\nSisa percobaan: {sisa_percobaan}")
                K.tanya_putih("Enter untuk kembali...")
        else:
            storage.username_aktif = nama_login
            return nama_login

    return ""
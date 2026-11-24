import KOLOR as K
from storage import akun, playlist, lagu_favorit


def buat_akun_baru():
    try:
        username_baru = K.tanya_cyan("\nBuat username: ").strip()
        password_baru = K.tanya_magenta("Buat password (minimal 8 karakter dan mengandung minimal 1 angka): ").strip()

        if username_baru == "" or password_baru == "":
            raise ValueError("Username dan password tidak boleh kosong.")

        if len(password_baru) < 8:
            raise ValueError("Password harus memiliki minimal 8 karakter.")

        if not any(char.isdigit() for char in password_baru):
            raise ValueError("Password harus mengandung setidaknya satu angka.")

        for nama in akun:
            if nama.lower() == username_baru.lower():
                raise ValueError("Username sudah digunakan.")

        akun[username_baru] = password_baru
        playlist[username_baru] = {}
        lagu_favorit[username_baru] = {}

    except ValueError as pesan_error:
        K.gagal(f"\n{pesan_error}")
    else:
        K.sukses("\nRegistrasi berhasil! Silakan login.")
    finally:
        K.tanya_putih("Enter untuk kembali...")
import KOLOR as K
from storage import akun, playlist  
def buat_akun_baru():
    username_baru = K.tanya_cyan("\nBuat username: ")
    password_baru = K.tanya_magenta("Buat password: ")
    if username_baru == "" or password_baru == "":
        K.gagal("\nUsername dan password tidak boleh kosong.")
    else: 
        username_sama = False
        for nama in akun:
            if nama.lower() == username_baru.lower():
                username_sama = True

        if username_sama == True:
            K.gagal("\nUsername sudah digunakan.")
        else:
            akun[username_baru] = password_baru
            playlist[username_baru] = {}
            K.sukses("\nRegistrasi berhasil! Silakan login.")
    K.tanya_putih("Enter untuk kembali...")
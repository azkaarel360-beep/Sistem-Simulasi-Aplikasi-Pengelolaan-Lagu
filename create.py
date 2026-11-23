from storage import akun, playlist, lagu_favorit

def buat_akun_baru():
    username_baru = input("\nBuat username: ").strip()
    password_baru = input("Buat password: ").strip()
    if username_baru == "" or password_baru == "":
        print("\nUsername dan password tidak boleh kosong.")
    else: 
        username_sama = False
        for nama in akun:
            if nama.lower() == username_baru.lower():
                username_sama = True

        if username_sama == True:
            print("\nUsername sudah digunakan.")
        else:
            akun[username_baru] = password_baru
            playlist[username_baru] = {}
            lagu_favorit[username_baru] = {}
            print("\nRegistrasi berhasil! Silakan login.")

    input("Enter untuk kembali...")
from colorama import init, Fore, Style

init(autoreset=True)

def _pesan(warna, simbol, teks):
    """Cetak newline di awal dulu, baru simbol + teks, supaya simbol tidak nyasar ke baris kosong."""
    isi = teks.lstrip("\n")
    print(teks[:len(teks) - len(isi)], end="")
    print(warna + simbol + " " + isi)

def sukses(teks):
    _pesan(Fore.GREEN, "✔", teks)

def gagal(teks):
    _pesan(Fore.RED , "✘", teks)

def peringatan(teks):
    _pesan(Fore.YELLOW , "⚠", teks)

def info(teks):
    _pesan(Fore.BLUE, "ℹ", teks)

def kosong(teks):
    print(Style.DIM + teks)

def judul(teks):
    print(Fore.CYAN + teks)

def daftar(teks):
    print(Fore.MAGENTA + teks)

def cetak_tabel(isi):
    print(Fore.LIGHTCYAN_EX + str(isi))

def tanya_yellow(teks):
    print(Fore.YELLOW + teks, end="")
    return input()

def tanya_hijau(teks):
    print(Fore.GREEN + teks, end="")
    return input()

def tanya_merah(teks):
    print(Fore.RED + teks, end="")
    return input()

def tanya_biru(teks):
    print(Fore.BLUE + teks, end="")
    return input()

def tanya_cyan(teks):
    print(Fore.CYAN + teks, end="")
    return input()

def tanya_magenta(teks):
    print(Fore.MAGENTA + teks, end="")
    return input()

def tanya_putih(teks):
    print(Fore.WHITE + teks, end="")
    return input()
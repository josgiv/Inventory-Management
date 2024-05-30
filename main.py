import subprocess
import os

def main_menu():
    """
    Menampilkan menu utama dan mengarahkan pengguna ke opsi yang dipilih.
    """
    while True:
        print("\n+--------------------------------------+")
        print("|              Menu Utama              |")
        print("+--------------------------------------+")
        print("| 1. Input Inventaris Baru             |")
        print("| 2. Input Inventaris Hilang/Rusak     |")
        print("| 3. Cek Inventaris                    |")
        print("| 4. Export CSV Laporan Inventaris     |")
        print("| 5. Keluar                            |")
        print("+--------------------------------------+")
        choice = input("Pilih opsi (1-5): ").strip().lower()
        
        if choice == '1':
            print('Anda memilih opsi Input Inventaris Baru.')
            subprocess.run(['python', os.path.join('app', 'input-inventory.py')])
        elif choice == '2':
            print('Anda memilih opsi Input Inventaris Hilang/Rusak.')
            subprocess.run(['python', os.path.join('app', 'input-defective.py')])
        elif choice == '3':
            print('Anda memilih opsi Cek Inventaris.')
            subprocess.run(['python', os.path.join('app', 'check-inventory.py')])
        elif choice == '4':
            print('Anda memilih opsi Export CSV Laporan Inventaris.')
            subprocess.run(['python', os.path.join('app', 'export-inventory.py')])
        elif choice == '5':
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid, silahkan coba lagi.")

if __name__ == "__main__":
    main_menu()

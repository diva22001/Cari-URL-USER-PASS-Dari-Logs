import os
import re
from tqdm import tqdm

def cari_file_password(file_path, output_file):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        matches = re.finditer(r'URL:(.*?)\nUsername:(.*?)\nPassword:(.*?)\n(.*?)===============', file_content, re.DOTALL)
        
        for match in matches:
            url = match.group(1).strip()
            username = match.group(2).strip()
            password = match.group(3).strip()

            # Skip baris yang mengandung kata 'UNKNOWN'
            if 'UNKNOWN' in url or 'UNKNOWN' in username or 'UNKNOWN' in password:
                continue

            gabung_data = f"{url}:{username}:{password}"

            with open(output_file, 'a', encoding='utf-8') as output_file:
                output_file.write(gabung_data + '\n')
    except Exception as e:
        # Jangan menampilkan pesan kesalahan jika gagal menyimpan
        pass

def cari_folder_password(root_folder, output_file):
    total_file_password = 0
    
    # Menggunakan tqdm untuk menunjukkan progres dalam persen
    for folder_path, _, files in tqdm(os.walk(root_folder), desc='Pencarian File Password', unit='folder', dynamic_ncols=True):
        for file_name in files:
            if file_name.lower() == 'passwords.txt':
                file_path = os.path.join(folder_path, file_name)
                cari_file_password(file_path, output_file)
                total_file_password += 1
    
    if total_file_password > 0:
        print(f"Total {total_file_password} file 'Passwords.txt' ditemukan.")
    else:
        print("Tidak ada file 'Passwords.txt' yang ditemukan.")

# Input dari pengguna untuk path folder utama
path_ke_folder_utama = input("Masukkan path folder utama: ")

# Ganti 'path_output_file' dengan path file tempat menyimpan hasil penggabungan
path_output_file = os.path.join(os.getcwd(), 'output.txt')

if os.path.exists(path_output_file):
    os.remove(path_output_file)

cari_folder_password(path_ke_folder_utama, path_output_file)

import os
import re
from tqdm import tqdm

def cari_file_password(file_path, output_file):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        # Set untuk menyimpan baris-baris unik
        unique_lines = set()

        # Pola pertama
        matches_pertama = re.finditer(r'URL:\s*(.*?)\nUsername:\s*(.*?)\nPassword:\s*(.*?)\n', file_content)
        for match in matches_pertama:
            url = match.group(1).strip()
            username = match.group(2).strip()
            password = match.group(3).strip()

            # Skip baris yang tidak memiliki URL, username, atau password atau mengandung kata '[NOT_SAVED]' atau 'UNKNOWN'
            if not url or not username or not password or '[NOT_SAVED]' in password or '[NOT_SAVED]' in username or 'UNKNOWN' in url or 'UNKNOWN' in username:
                continue

            gabung_data = f"{url}:{username}:{password}"
            unique_lines.add(gabung_data)

        # Pola kedua
        matches_kedua = re.finditer(r'URL:\s*(.*?)\nLogin:\s*(.*?)\nPassword:\s*(.*?)\n', file_content)
        for match in matches_kedua:
            url = match.group(1).strip()
            login = match.group(2).strip()
            password = match.group(3).strip()

            # Skip baris yang tidak memiliki URL, login, atau password atau mengandung kata '[NOT_SAVED]' atau 'UNKNOWN'
            if not url or not password or '[NOT_SAVED]' in password or 'UNKNOWN' in url or 'UNKNOWN' in login:
                continue

            gabung_data = f"{url}:{login}:{password}"
            unique_lines.add(gabung_data)

        # Pola ketiga
        matches_ketiga = re.finditer(r'SOFT:\s*(.*?)\nURL:\s*(.*?)\nUSER:\s*(.*?)\nPASS:\s*(.*?)\n', file_content)
        for match in matches_ketiga:
            soft = match.group(1).strip()
            url = match.group(2).strip()
            username = match.group(3).strip()
            password = match.group(4).strip()

            # Skip baris yang tidak memiliki URL, username, atau password atau mengandung kata '[NOT_SAVED]' atau 'UNKNOWN'
            if not url or not username or not password or '[NOT_SAVED]' in password or '[NOT_SAVED]' in username or 'UNKNOWN' in url or 'UNKNOWN' in username:
                continue

            gabung_data = f"{url}:{username}:{password}"
            unique_lines.add(gabung_data)

        # Pola keempat
        matches_keempat = re.finditer(r'URL:\s*(.*?)\nUsername:\s*(.*?)\nPassword:\s*(.*?)\nApplication:', file_content)
        for match in matches_keempat:
            url = match.group(1).strip()
            username = match.group(2).strip()
            password = match.group(3).strip()

            # Skip baris yang tidak memiliki URL, username, atau password atau mengandung kata '[NOT_SAVED]' atau 'UNKNOWN'
            if not url or not username or not password or '[NOT_SAVED]' in password or '[NOT_SAVED]' in username or 'UNKNOWN' in url or 'UNKNOWN' in username:
                continue

            gabung_data = f"{url}:{username}:{password}"
            unique_lines.add(gabung_data)

        # Menuliskan baris-baris unik ke file output
        with open(output_file, 'a', encoding='utf-8') as output_file:
            for line in unique_lines:
                output_file.write(line + '\n')

    except Exception as e:
        # Jangan menampilkan pesan kesalahan jika gagal menyimpan
        pass

def cari_folder_password(root_folder, output_file):
    total_file_password = 0
    
    # Menggunakan tqdm untuk menunjukkan progres dalam persen
    for folder_path, _, files in tqdm(os.walk(root_folder), desc='Pencarian File Password', unit='folder', dynamic_ncols=True):
        for file_name in files:
            # Mencari file .txt yang mengandung kata "passwords" dalam namanya
            if file_name.lower().endswith('.txt') and 'passwords' in file_name.lower():
                file_path = os.path.join(folder_path, file_name)
                cari_file_password(file_path, output_file)
                total_file_password += 1
    
    if total_file_password > 0:
        print(f"Total {total_file_password} file '.txt' yang mengandung kata 'passwords' ditemukan.")
    else:
        print("Tidak ada file '.txt' yang mengandung kata 'passwords' yang ditemukan.")

# Input dari pengguna untuk path folder utama
path_ke_folder_utama = input("Masukkan path folder utama: ")

# Ganti 'path_output_file' dengan path file tempat menyimpan hasil penggabungan
path_output_file = os.path.join(os.getcwd(), 'output.txt')

if os.path.exists(path_output_file):
    os.remove(path_output_file)

cari_folder_password(path_ke_folder_utama, path_output_file)

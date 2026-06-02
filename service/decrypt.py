#!/usr/bin/env python3

import os
import sys
import shutil

from tqdm import tqdm
from getpass import getpass
from cryptography.fernet import Fernet
from core.kdf import derive_key_from_password
from core.zip_manager import extract_zip
from core.file_scanner import collect_files
from core.fernet_engine import decrypt_file
from core.colors import color


def main():

    while True:
        target_dir = input(color.BOLD + "Enter folder containing CRYPT zip: " + color.END).strip()

        if not os.path.isdir(target_dir):
            print(color.BOLD + color.ORANGE + "Invalid folder" + color.END) 
            continue

        target_dir = os.path.abspath(target_dir)

        zip_files = [
        f for f in os.listdir(target_dir)
        if f.startswith("CRYPT") and f.endswith(".zip")
        ]

        if not zip_files:
            print(color.BOLD + color.ORANGE + "No ZIP found" + color.END)
            continue

        break

    while True:
        print(color.BOLD + "\nAvailable encrypted archives:\n" + color.END)

        for i, z in enumerate(zip_files, 1):
            print(f"[{i}] {z}")

        try:
            choice = int(input(color.BOLD + "\nSelect ZIP to decrypt (number): "+ color.END))

            if not (1 <= choice <= len(zip_files)):
                print(color.BOLD + color.ORANGE + "Invalid selection" + color.END)
                continue

        except ValueError:
            print(color.BOLD + "Please enter a number" + color.END)
            continue

        zip_name = zip_files[choice - 1]
        zip_path = os.path.join(target_dir, zip_name)

        print(f"\nSelected: {zip_name}")

        confirm = input(color.BOLD + color.YELLOW + "Proceed with decryption? (Y/N) Default [Y]: " + color.END).strip().lower()

        if confirm == "y" or choice == "":
            break

        elif confirm == "n":
            print(color.BOLD + "Okay, choose again...\n" + color.END)
            continue

        else:
            print(color.BOLD + color.ORANGE + "Invalid input\n" + color.END)


    zip_base = os.path.splitext(zip_name)[0]

    extract_folder = os.path.join(target_dir, zip_base)
    while True:
        zip_password = getpass(color.BOLD + "ZIP password: " + color.END)

        try:
            extract_zip(zip_path, extract_folder, zip_password)

        except ValueError as e:
            print(color.BOLD + color.RED + f"ERROR: {e}" + color.END)
            continue

        except Exception as e:
            print(color.BOLD + color.RED + f"Extraction failed: {e}" + color.END)
            continue
        break

    while True:
        decrypt_password = getpass(color.BOLD + "Decryption password: " + color.END)

        meta_dir = os.path.join(extract_folder, ".metadata")

        if not os.path.exists(meta_dir):
            print(color.BOLD + color.RED + "ERROR: Missing metadata folder in archive." + color.END)
            break  # go back to ZIP selection

        salt_path = os.path.join(meta_dir, "salt.bin")
        key_path = os.path.join(meta_dir, "encryptionKey.key")

        try:
            with open(salt_path, "rb") as f:
                salt = f.read()

            with open(key_path, "rb") as f:
                encrypted_file_key = f.read()

        except Exception:
            print(color.BOLD + color.RED + "ERROR: Missing or corrupted metadata files." + color.END)
            break  # go back to ZIP selection

        try:
            password_key = derive_key_from_password(decrypt_password, salt)
            file_key = Fernet(password_key).decrypt(encrypted_file_key)

        except Exception:
            print(color.BOLD + color.RED + "ERROR: Wrong decryption password or corrupted key." + color.END)
            continue  # retry password only

        files = [
            f for f in collect_files(extract_folder)
            if ".metadata" not in f
        ]

        if not files:
            print(color.BOLD + color.ORANGE + "No files found in extracted archive." + color.END)
            break  # IMPORTANT: go back to ZIP selection

        break

    fernet = Fernet(file_key)

    print(color.BOLD + "Decrypting files...\n" + color.END)

    for f in tqdm(files, desc=color.BOLD + "Decrypting" + color.END, unit="file", ncols=90):
        decrypt_file(f, fernet)

    print(color.BOLD + "\nDecrypted files...\n" + color.END)

    for f in files:
        print(f)

    print(color.BOLD + color.UNDERLINE + f"\nTotal files: {len(files)}\n" + color.END) 

    shutil.rmtree(meta_dir)

    print(color.BOLD + color.GREEN + color.UNDERLINE + "\nDECRYPTION COMPLETE" + color.END)
    print(f"Output folder: {extract_folder}")


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print(color.BOLD + color.RED + "\nOperation cancelled by user." + color.END)
        sys.exit(0)

    except Exception as e:
        print(color.BOLD + color.RED + f"Fatal error: {e}" + color.END)
        sys.exit(1)
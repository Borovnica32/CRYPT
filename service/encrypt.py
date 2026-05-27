#!/usr/bin/env python3

import os
import sys
import platform
import subprocess
import shutil

from tqdm import tqdm
from datetime import datetime
from getpass import getpass
from cryptography.fernet import Fernet
from core.kdf import derive_key_from_password
from core.file_scanner import collect_files
from core.fernet_engine import encrypt_file
from core.zip_manager import create_zip
from core.password_policy import validate_password
from core.colors import color


def main():

    while True:
        target_dir = input(color.BOLD + "Enter folder path to encrypt: " + color.END).strip()

        if not os.path.isdir(target_dir):
            print(color.BOLD + color.ORANGE + "Invalid folder path" + color.END)
            continue

        target_dir = os.path.abspath(target_dir)

        files = collect_files(target_dir)

        if not files:
            print(color.BOLD + color.ORANGE + "No files found in this folder. Try another path." + color.END)
            continue

        print(color.BOLD + "\nFiles to be encrypted...\n" + color.END)
        for f in files:
            print(f)

        print(color.BOLD + color.UNDERLINE + f"\nTotal files: {len(files)}\n" + color.END)

        break

    while True:
        password = getpass(color.BOLD + "Create encryption password: " + color.END)

        ok, msg = validate_password(password)
        if not ok:
            print(msg)
            continue

        password_confirm = getpass(color.BOLD + "Confirm password: " + color.END)

        if password != password_confirm:
            print(color.BOLD + color.ORANGE + "Passwords do not match." + color.END)
            continue

        break

    while True:
        choice = input(color.YELLOW + color.BOLD + "Continue and encrypt? (Y/N) Default [Y]: " + color.END).strip().lower()

        if choice == "n":
            print(color.BOLD + "Encryption cancelled by user." + color.END)
            sys.exit(0)

        elif choice == "y" or choice == "":
            break

        else:
            print(color.BOLD + color.ORANGE + "Invalid choice" + color.END)


    output_dir = os.path.join(target_dir, ".tmp")
    meta_dir = os.path.join(target_dir, ".metadata")

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(meta_dir, exist_ok=True)

    # hide metadata folder (Windows only)
    if platform.system() == "Windows":
        subprocess.call(['attrib', '+h', meta_dir])


    salt = os.urandom(16)

    file_key = Fernet.generate_key()
    password_key = derive_key_from_password(password, salt)

    encrypted_file_key = Fernet(password_key).encrypt(file_key)

    # save metadata
    salt_path = os.path.join(meta_dir, "salt.bin")
    key_path = os.path.join(meta_dir, "encryptionKey.key")

    with open(salt_path, "wb") as f:
        f.write(salt)

    with open(key_path, "wb") as f:
        f.write(encrypted_file_key)

    fernet = Fernet(file_key)

    print(color.BOLD + "\nEncrypting files...\n" + color.END)

    for f in tqdm(files, desc="Encrypting", unit="file", ncols=90):

        rel_path = os.path.relpath(f, target_dir)
        output_path = os.path.join(output_dir, rel_path)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        encrypt_file(f, output_path, fernet)


    while True:
        choice = input(color.BOLD + color.YELLOW + "Use same password for ZIP? (Y/N) Default [N]: " + color.END).strip().lower()

        if choice == "y":
            zip_password = password
            break

        elif choice == "n" or choice == "":
            while True:
                zip_password = getpass(color.BOLD + "Enter ZIP password: " + color.END)
                zip_confirm = getpass(color.BOLD + "Confirm ZIP password: " + color.END)

                if zip_password != zip_confirm:
                    print(color.BOLD + color.ORANGE + "Passwords do not match." + color.END)
                    continue
                break
            break

        else:
            print(color.BOLD + color.ORANGE + "Invalid choice" + color.END)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    zip_path = os.path.join(target_dir, f"CRYPT-{timestamp}.zip")

    encrypted_files = collect_files(output_dir)

    create_zip(
        zip_path=zip_path,
        files=encrypted_files,
        base_dir=output_dir,
        password=zip_password,
        extra_files=[key_path, salt_path]
    )

    # Delete tmp and metadata folders
    shutil.rmtree(meta_dir)
    shutil.rmtree(output_dir)


    print(color.UNDERLINE + color.BOLD + color.GREEN + "\nENCRYPTION COMPLETE" + color.END)


if __name__ == "__main__":
    try:
        main()

    # User interupted the process
    except KeyboardInterrupt:
        print(color.UNDERLINE + color.BOLD + "\nOperation cancelled by user." + color.END)
        sys.exit(0)

    # An error occured
    except Exception as e:
        print(color.UNDERLINE + color.RED + f"Fatal error: {e}" + color.END)
        sys.exit(1)
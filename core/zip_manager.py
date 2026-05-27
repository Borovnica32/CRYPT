import os
import pyzipper
import zipfile
from tqdm import tqdm
from core.colors import color


def create_zip(zip_path, files, base_dir, password, extra_files=None):

    print(color.BOLD + "\nBUILDING ARCHIVE...\n" + color.END)

    with pyzipper.AESZipFile(
        zip_path,
        'w',
        compression=zipfile.ZIP_DEFLATED,
        encryption=pyzipper.WZ_AES
    ) as zipf:

        zipf.setpassword(password.encode())

        # MAIN FILES
        for f in tqdm(files, desc="Zipping files", unit="file", ncols=90):
            arcname = os.path.relpath(f, base_dir)
            zipf.write(f, arcname)

        # METADATA FILES
        if extra_files:
            print("\nAdding metadata files...\n")

            for f in extra_files:
                arcname = os.path.join(".metadata", os.path.basename(f))
                zipf.write(f, arcname)

    print(color.UNDERLINE + color.BOLD + "\nZIP creation complete." + color.END)

def extract_zip(zip_path, extract_folder, password):

    print(color.BOLD + "\nEXTRACTING ARCHIVE...\n" + color.END)

    with pyzipper.AESZipFile(zip_path) as zipf:
        zipf.setpassword(password.encode())

        file_list = zipf.namelist()

        if not file_list:
            raise ValueError("Empty ZIP file")

        # password check
        try:
            with zipf.open(file_list[0]) as f:
                f.read(1)
        except RuntimeError:
            raise ValueError("Incorrect ZIP password")

        os.makedirs(extract_folder, exist_ok=True)

        for file in tqdm(file_list, desc="Extracting", unit="file", ncols=90):
            zipf.extract(file, extract_folder)

    print(color.GREEN + "ZIP extracted successfully." + color.END)
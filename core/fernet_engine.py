from cryptography.fernet import Fernet


def encrypt_file(input_path, output_path, fernet: Fernet):

    with open(input_path, "rb") as f:
        data = f.read()

    encrypted = fernet.encrypt(data)

    with open(output_path, "wb") as f:
        f.write(encrypted)


def decrypt_file(path: str, fernet: Fernet):
    with open(path, "rb") as f:
        data = f.read()
    dec = fernet.decrypt(data)
    with open(path, "wb") as f:
        f.write(dec)
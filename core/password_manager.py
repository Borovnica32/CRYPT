import base64
import random

def save_passwd(file_path, text_to_append):
    try:
        with open(file_path, 'a') as file:
            file.write(text_to_append + '\n')

        print(f"\nPassword saved to {file_path} successfully.")

    except Exception as e:
        print(f"Error: {e}")

def encode_passwd(passwd):
    password_bytes = passwd.encode("ascii")

    base64_bytes = base64.b64encode(password_bytes)
    base64_string = base64_bytes.decode("ascii")

    return base64_string


def decode_passwd(encoded: str) -> str:
    return base64.b64decode(encoded.encode("ascii")).decode("ascii")

def load_passwords(file_path):
    passwords = []

    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or ":" not in line:
                    continue

                service, encoded = line.split(":", 1)
                passwords.append((service.strip(), encoded.strip()))

    except FileNotFoundError:
        print("No password file found.")
        return []

    return passwords

def update_password(file_path, service_name, new_encoded_password):
    lines = []

    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Password file not found.")
        return False

    updated = False

    for i, line in enumerate(lines):
        if line.startswith(service_name + ":"):
            lines[i] = f"{service_name}: {new_encoded_password}\n"
            updated = True
            break

    if not updated:
        print("Service not found.")
        return False

    with open(file_path, "w") as f:
        f.writelines(lines)

    return True

def generate_password(length, include_nums=True, include_spec=True):
    alpha = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    nums = list("0123456789")
    spec = list("!@#$%^&*()-_=+[]{}|;:,.<>?/`~")

    pool = alpha[:]

    if include_nums:
        pool += nums
    if include_spec:
        pool += spec

    return "".join(random.choice(pool) for _ in range(length))

def interactive_password_generator():
    while True:
        try:
            length = int(input("Provide password length: "))
            if length <= 0:
                print("Length must be greater than 0")
                continue
            break
        except ValueError:
            print("Value must be an integer")

    include_nums = input("Include numbers? (Y/N): ").strip().lower() != "n"
    include_spec = input("Include special chars? (Y/N): ").strip().lower() != "n"

    return generate_password(length, include_nums, include_spec)
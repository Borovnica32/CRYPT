import base64

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
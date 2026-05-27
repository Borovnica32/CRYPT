import os
import sys

from core.password_manager import load_passwords, decode_passwd
from core.colors import color

def main():

    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "shadow", "passwd.txt")

    passwords = load_passwords(file_path)

    if not passwords:
        print("No saved passwords found.")
        return

    print("\nAvailable passwords:\n")

    for i, (service, _) in enumerate(passwords, 1):
        print(f"[{i}] {service}")

    while True:
        try:
            choice = int(input("\nSelect password to decode: "))
            if 1 <= choice <= len(passwords):
                break
            print("Invalid selection")
        except ValueError:
            print("Enter a number")

    service, encoded = passwords[choice - 1]

    decoded = decode_passwd(encoded)

    print("\nSelected service:", service)
    print("Password:", decoded)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print(color.BOLD + color.RED + "\nOperation cancelled by user." + color.END)
        sys.exit(0)

    except Exception as e:
        print(color.BOLD + color.RED + f"Fatal error: {e}" + color.END)
        sys.exit(1)
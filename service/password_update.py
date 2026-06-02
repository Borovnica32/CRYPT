#!/usr/bin/env python3

import sys
from core.colors import color
from core.password_manager import (
    interactive_password_generator,
    encode_passwd
)

from core.password_db import (
    init_db,
    get_all_services,
    update_password
)

def main():
    init_db()

    services = get_all_services()

    if not services:
        print("No passwords stored.")
        return

    print("\nStored services:\n")
    for i, s in enumerate(services, 1):
        print(f"[{i}] {s}")

    while True:
        try:
            choice = int(input("\nSelect service to update: "))
            if 1 <= choice <= len(services):
                break
            print("Invalid selection")
        except ValueError:
            print("Enter a number")

    service = services[choice - 1]

    mode = input("Generate new password? (Y/N): ").strip().lower()

    if mode == "y":
        new_password = interactive_password_generator()
        print("\nNew password:", new_password)

    else:
        while True:
            new_password = input("Enter new password: ").strip()
            confirm = input("Confirm: ").strip()

            if new_password == confirm:
                break
            print("Mismatch")

    update_password(service, encode_passwd(new_password))

    print("\nUpdated successfully.")


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print(color.BOLD + color.RED + "\nCancelled." + color.END)
        sys.exit(0)
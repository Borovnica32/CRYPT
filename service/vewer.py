#!/usr/bin/env python3

import sys
from core.colors import color
from core.password_manager import decode_passwd
from core.password_db import init_db, get_all_services, get_password


def main():
    init_db()

    services = get_all_services()

    if not services:
        print("No saved passwords found.")
        return

    print("\nAvailable passwords:\n")

    for i, s in enumerate(services, 1):
        print(f"[{i}] {s}")

    # select service
    while True:
        try:
            choice = int(input("\nSelect password to view: "))
            if 1 <= choice <= len(services):
                break
            print("Invalid selection")
        except ValueError:
            print("Enter a number")

    service = services[choice - 1]

    encoded = get_password(service)

    if not encoded:
        print("Password not found in database.")
        return

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
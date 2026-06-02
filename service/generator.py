#!/usr/bin/env python3

import sys
from core.colors import color
from core.password_manager import (
    interactive_password_generator,
    encode_passwd
)

from core.password_db import init_db, add_password


def main():
    init_db()

    service = input("Enter service: ").strip()

    password = interactive_password_generator()

    print("\nGenerated password:", password)

    encoded = encode_passwd(password)

    add_password(service, encoded)

    print("\nSaved to SQLite database.")


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print(color.BOLD + color.RED + "\nCancelled." + color.END)
        sys.exit(0)
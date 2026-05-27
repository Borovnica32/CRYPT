import random
import os

from core.password_manager import save_passwd

def main():

    alpha = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    nums = list("0123456789")
    spec = list("!@#$%^&*()-_=+[]{}|;:,.<>?/`~")

    include_nums = True
    include_spec = True

    service = input("Enter the service this password is for: ").strip()

    # length input
    while True:
        try:
            length = int(input("Provide password length: "))
            if length <= 0:
                print("Length must be greater than 0")
                continue
            break
        except ValueError:
            print("Value must be an integer")

    # options
    choice = input("Include numbers? (Y/N): ").strip().lower()
    if choice == "n":
        include_nums = False

    choice = input("Include special chars? (Y/N): ").strip().lower()
    if choice == "n":
        include_spec = False

    pool = alpha[:]

    if include_nums:
        pool += nums

    if include_spec:
        pool += spec

    # generate password
    password = "".join(random.choice(pool) for _ in range(length))

    print("\nGenerated password:")
    print(password)

    # safe path (relative to project root)
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "shadow", "passwd.txt")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    save_passwd(file_path, f"{service}: {password}")

    print("\nSaved to shadow/passwd.txt")

if __name__ == "__main__":
    main()
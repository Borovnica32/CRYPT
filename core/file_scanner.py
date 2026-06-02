import os

SKIP_FILES = {
    "encrypt.py",
    "decrypt.py",
    "generator.py",
    "encryptionKey.key",
    "salt.bin",
    "encrypt.exe",
    "decrypt.exe",
    "generator.exe"
}

SKIP_DIRS = {"__pycache__", ".git", ".venv", ".metadata"}

def collect_files(root_dir: str):
    files = []

    for root, dirs, filenames in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for filename in filenames:
            if filename in SKIP_FILES:
                continue
            if filename.endswith(".py"):
                continue

            files.append(os.path.join(root, filename))

    return files
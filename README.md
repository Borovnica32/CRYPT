# CRYPT

A lightweight command-line file encryption and password utility written in Python.

CRYPT is split into two main components:

- **File encryption** — encrypt a folder's files with Fernet, then package the encrypted files into a password-protected AES ZIP archive.
- **Password utility** — generate, store, update, and view passwords using a local SQLite database.

> **Status:** Personal / experimental project. Use it for learning and controlled environments rather than as a production-grade password manager or backup system.

## Features

### File encryption

- Recursively scans a target folder.
- Encrypts files using `cryptography.fernet.Fernet`.
- Derives an encryption key from a password using **PBKDF2-HMAC-SHA256**.
- Uses a random 16-byte salt for password-based key derivation.
- Generates a separate random Fernet file key.
- Encrypts the file key with the password-derived key.
- Stores the encrypted file key and salt as archive metadata.
- Packages the encrypted files into a password-protected ZIP archive using **AES encryption** through `pyzipper`.
- Creates timestamped archives in the format:

```text
CRYPT-YYYYMMDD_HHMMSS.zip
```

### Password utility

The password utility provides:

- Random password generation
- Configurable password length
- Optional numbers
- Optional special characters
- Password generation for named services
- Updating existing stored passwords
- Viewing stored passwords
- SQLite storage in `shadow/shadow.db`

## Project structure

```text
CRYPT/
├── core/
│   ├── colors.py
│   ├── fernet_engine.py
│   ├── file_scanner.py
│   ├── kdf.py
│   ├── password_db.py
│   ├── password_manager.py
│   ├── password_policy.py
│   └── zip_manager.py
│
├── service/
│   ├── encrypt.py
│   ├── decrypt.py
│   ├── generator.py
│   ├── updater.py
│   └── vewer.py
│
└── shadow/
    └── shadow.db
```

## Requirements

CRYPT requires Python 3 and the following third-party packages:

- `cryptography`
- `pyzipper`
- `tqdm`

The password utility itself uses Python's built-in `sqlite3` module.

## Installation

Clone the repository:

```bash
git clone https://github.com/Borovnica32/CRYPT.git
cd CRYPT
```

Creating a virtual environment is recommended.

### Windows

```powershell
py -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install cryptography pyzipper tqdm
```

You can also create a `requirements.txt` containing:

```text
cryptography
pyzipper
tqdm
```

and install it with:

```bash
python -m pip install -r requirements.txt
```

## Usage

### Encrypt a folder

Run:

```bash
python service/encrypt.py
```

CRYPT will ask for the folder to encrypt.

It will then:

1. Scan the folder for files.
2. Display the files that will be encrypted.
3. Ask for an encryption password.
4. Validate the password.
5. Encrypt the files.
6. Ask whether the ZIP should use the same password.
7. Create a timestamped `CRYPT-*.zip` archive.
8. Remove temporary encryption data after the archive is created.

Example:

```text
Enter folder path to encrypt: C:\Users\User\Documents\Test

Files to be encrypted...

C:\Users\User\Documents\Test\document.pdf
C:\Users\User\Documents\Test\photo.jpg

Total files: 2

Create encryption password:
Confirm password:

Continue and encrypt? (Y/N) Default [Y]:

Use same password for ZIP? (Y/N) Default [N]:
```

### Decrypt an archive

Run:

```bash
python service/decrypt.py
```

Enter the folder containing the `CRYPT-*.zip` archive.

CRYPT will:

1. Find available CRYPT archives.
2. Let you select an archive.
3. Ask for the ZIP password.
4. Extract the archive.
5. Read the encrypted file key and salt from `.metadata`.
6. Derive the key from the decryption password.
7. Recover the original Fernet file key.
8. Decrypt the files in the extracted directory.
9. Remove the extracted metadata directory.

## Password utility

### Generate a password

Run:

```bash
python service/generator.py
```

The program asks for a service name and password settings, generates a password, and stores it in the SQLite database.

### Update a password

Run:

```bash
python service/updater.py
```

Select an existing service and either generate a new password or enter one manually.

### View a password

Run:

```bash
python service/vewer.py
```

> The file is currently named `vewer.py` in the project. This is the existing filename and can be renamed to `viewer.py` later if desired.

## Encryption design

The file-encryption workflow uses two keys.

### 1. File key

A random Fernet key is generated for the files:

```text
Fernet.generate_key()
```

Each file is encrypted with this key.

### 2. Password-derived key

The user's password is processed using:

```text
PBKDF2-HMAC-SHA256
390,000 iterations
32-byte derived key
random 16-byte salt
```

The random file key is then encrypted with the password-derived key.

Conceptually:

```text
User password
     │
     ▼
PBKDF2-HMAC-SHA256
     │
     ├── random salt
     ▼
Password-derived key
     │
     ▼
Encrypt random file key
     │
     ▼
Encrypted file key
```

The archive contains the encrypted files plus metadata required to recover the file key:

```text
CRYPT-YYYYMMDD_HHMMSS.zip
├── encrypted files...
└── .metadata/
    ├── encryptionKey.key
    └── salt.bin
```

## Password policy

Encryption passwords currently must:

- contain at least 8 characters
- contain at least one number
- contain at least one special character

For example:

```text
MySecurePassword123!
```

## Important security notes

CRYPT is an educational/personal project and should not currently be treated as a production security tool.

### Password utility

The password utility currently stores passwords using **Base64 encoding**.

Base64 is **encoding, not encryption**.

Therefore, anyone who obtains `shadow/shadow.db` can decode the stored passwords.

Do not use the current password utility for storing important real-world passwords unless this part of the project is redesigned.

### File encryption

The file-encryption component uses real cryptographic primitives (`Fernet` and PBKDF2), but the overall application has not been independently security audited.

Keep backups of important data and test the decryption process before trusting an archive with important files.

## Files excluded from encryption

The file scanner intentionally ignores:

```text
__pycache__
.git
.venv
.metadata
```

It also skips Python source files and several CRYPT-specific files.

This prevents CRYPT's own application files and temporary metadata from accidentally being included in an encryption operation.

## Development

Recommended local setup:

```bash
git clone https://github.com/Borovnica32/CRYPT.git
cd CRYPT

python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install cryptography pyzipper tqdm
```

Then run one of the services:

```bash
python service/encrypt.py
python service/decrypt.py
python service/generator.py
python service/updater.py
python service/vewer.py
```

## Planned improvements

Possible future improvements include:

- [ ] Add `requirements.txt`
- [ ] Add `.gitignore`
- [ ] Rename `vewer.py` to `viewer.py`
- [ ] Replace Base64 password storage with proper password encryption / protected secrets
- [ ] Add authentication for the password database
- [ ] Add automated tests
- [ ] Add command-line arguments instead of interactive prompts
- [ ] Improve error handling and recovery after interrupted encryption
- [ ] Add archive integrity checks
- [ ] Add logging
- [ ] Improve cross-platform behavior
- [ ] Add a proper release/package structure
- [ ] Add CI testing with GitHub Actions

## Disclaimer

CRYPT is provided as a personal/educational project. Always keep an independent backup of important data and verify that encrypted archives can be successfully decrypted before relying on them.

## License

No license is currently specified for this repository.

If this project is intended to be publicly reused or distributed, consider adding an appropriate open-source license.

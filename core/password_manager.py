def save_passwd(file_path, text_to_append):
    try:
        with open(file_path, 'a') as file:
            file.write(text_to_append + '\n')

        print(f"\nPassword saved to {file_path} successfully.")

    except Exception as e:
        print(f"Error: {e}")
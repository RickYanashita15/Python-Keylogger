from cryptography.fernet import Fernet

key = "aK9Aamh-txCxirHhCLEZ-phPxpQRUTEXhBHigOeF30Q="

system_information_encrypted = "e_system.txt"
clipboard_information_encrypted = "e_clipboard.txt"
keys_information_encrypted = "e_keys_logged_txt"

encrypted_files = [system_information_encrypted, clipboard_information_encrypted, keys_information_encrypted]
count = 0

for decrypting_file in encrypted_files:

    with open(encrypted_files[count], "rb") as f:
        data = f.read()
    
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open(encrypted_files[count], "wb") as f:
        f.write(decrypted)
    
    count += 1 
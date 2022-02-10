from socket import *

PORT = 12000

def save_to_file(log):
    with open("log.txt", "a") as f:
        print(log, file=f)
    print("[+] log saved to file")
    
if __name__ == "__main__":
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', PORT)) # imposto il socket sul localhost porta PORT
    serverSocket.listen(1)

    file = open("log.txt", "r+")
    file.truncate(0);
    file.close();

    while 1:
        connectionSocket, addr = serverSocket.accept()
        data = connectionSocket.recv(1024)
        data = str(data, 'utf-8')
        print(data)
        save_to_file(data)

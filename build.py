import os
import shutil
import subprocess

def build():
    # 1. Cura?are build-uri vechi
    for folder in ['build', 'dist', 'release']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    os.makedirs('release')

    # 2. Comanda PyInstaller
    print('?? Construire executabil...')
    cmd = [
        'pyinstaller',
        '--noconfirm',
        '--onefile',
        '--windowed',
        '--name', 'AnexaAcademy',
        '--add-data', 'client/src/styles;client/src/styles',
        '--collect-all', 'PySide6',
        'client/src/main.py'
    ]
    subprocess.run(cmd)

    # 3. Mutare in release
    if os.path.exists('dist/AnexaAcademy.exe'):
        shutil.move('dist/AnexaAcademy.exe', 'release/AnexaAcademy.exe')
        print(f'? Build complet! Executabilul se afla in folderul release/')

if __name__ == '__main__':
    build()

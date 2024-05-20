import PyInstaller.__main__

PyInstaller.__main__.run([
    'building_example.py',
    '--name', 'pyinstaller_build.exe',
    '--onefile',
    '--add-data', 'assets;assets'
])
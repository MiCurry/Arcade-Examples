import subprocess

EXECUTABLE_NAME = "nuitka_build.exe"
DATA_DIRECTORY_SPEC = "assets=assets"

nuitka_command = [
    'python3.11.exe', '-m', 'nuitka',
    f'--output-filename={EXECUTABLE_NAME}',
    f'--include-data-dir={DATA_DIRECTORY_SPEC}',
    '--output-dir=dist',
    '--remove-output',
    './building_example.py',
    '--standalone',
    '--onefile'
]

subprocess.run(nuitka_command)
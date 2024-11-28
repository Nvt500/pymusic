import PyInstaller.__main__


PyInstaller.__main__.run([
    "src/pymusic.py",
    "--onefile",
    "--console",
    "--distpath",
    "executable",
    "--workpath",
    "executable",
    "--specpath",
    "executable",
])

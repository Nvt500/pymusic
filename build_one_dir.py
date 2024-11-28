import PyInstaller.__main__


PyInstaller.__main__.run([
    "src/pymusic.py",
    "--onedir",
    "--console",
    "--distpath",
    "executable",
    "--workpath",
    "executable/build",
    "--specpath",
    "executable",
])

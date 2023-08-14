import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_exe_options = {
    "packages": ["sys", "os", "pickle", "pandas", "openpyxl", "PyQt5"],
    "include_files": ["bk3data.xlsx"],
    "excludes": []
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "ListViewDemo",
    version = "0.1",
    description = "Autocomplete Search",
    options = {"build_exe": build_exe_options},
    executables = [Executable("bk3sort.py", base=base)]
)

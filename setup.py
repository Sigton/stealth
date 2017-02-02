import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="Stealth",
    options={
        "build_exe": {
            "packages": ["pygame", "json", "os"],
            "excludes": ["tkinter", "OpenGL"],
            "include_files": ["source/"]
        }
    },
    executables=executables
)

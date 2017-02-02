import cx_Freeze

executables = [cx_Freeze.Executable("source/main.py")]

include_files = ["source/level_data/",
                 "source/resources/",
                 "source/arms.py",
                 "source/constants.py",
                 "source/covers.py",
                 "source/entities.py",
                 "source/guards.py",
                 "source/healthbar.py",
                 "source/level.py",
                 "source/leveltext.py",
                 "source/platforms.py",
                 "source/player.py",
                 "source/spritesheet.py",
                 "source/terrain.py",
                 "source/torches.py"]

excludes = ["tkinter",
            "OpenGL",
            "email",
            "html",
            "http",
            "multiprocessing",
            "numpy",
            "urllib",
            "xml",
            "socket"]

cx_Freeze.setup(
    name="Stealth",
    options={
        "build_exe": {
            "packages": ["pygame", "json", "os"],
            "excludes": excludes,
            "include_files": include_files
        }
    },
    executables=executables
)

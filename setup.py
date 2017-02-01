import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="Stealth",
    options={
        "build_exe": {
            "packages": ["pygame", "json", "os"],
            "excludes": ["tkinter"],
            "include_files": [
                "level_data/",
                "resources/",
                "constants.py",
                "covers.py",
                "entities.py",
                "guards.py",
                "healthbar.py",
                "level.py",
                "leveltext.py",
                "platforms.py",
                "player.py",
                "spritesheet.py",
                "terrain.py",
                "torches.py"
            ]
        }
    },
    executables=executables
)

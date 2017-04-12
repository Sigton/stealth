import cx_Freeze

executables = [cx_Freeze.Executable(script="source/main.py",
                                    icon="source/resources/icon.ico",
                                    targetName="Stealth.exe")]

include_files = ["source/level_data/",
                 "source/resources/",
                 "source/guard_parts.py",
                 "source/constants.py",
                 "source/covers.py",
                 "source/entities.py",
                 "source/guards.py",
                 "source/progressbar.py",
                 "source/level.py",
                 "source/text.py",
                 "source/platforms.py",
                 "source/player.py",
                 "source/spritesheet.py",
                 "source/terrain.py",
                 "source/torches.py",
                 "source/funcs.py",
                 "source/game.py",
                 "source/menu.py",
                 "source/hud.py",
                 "source/saves.py",
                 "source/sounds.py",
                 "source/intros.py",
                 "source/save_data.json"]

excludes = ["OpenGL",
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
            "packages": ["pygame", "json", "os", "random", "PIL", "GIFImage"],
            "excludes": excludes,
            "include_files": include_files
        }
    },
    executables=executables
)

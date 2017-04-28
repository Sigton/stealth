import cx_Freeze
import py_compile
import os

# First of compile of the source files, since they
# take up less storage space when compiled

source_files = ["source/guard_parts.py",
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
                "source/GIFImage.py"]

# Compile each of the source files
for file in source_files:
    py_compile.compile(file, os.path.join("compiled", file[7:]+"c"))

# Set up the executable
executables = [cx_Freeze.Executable(script="source/main.py",
                                    icon="source/resources/icon.ico",
                                    targetName="Stealth.exe")]

# All of the files that need to be included
include_files = ["source/level_data/",
                 "source/resources/",
                 "compiled/guard_parts.pyc",
                 "compiled/constants.pyc",
                 "compiled/covers.pyc",
                 "compiled/entities.pyc",
                 "compiled/guards.pyc",
                 "compiled/progressbar.pyc",
                 "compiled/level.pyc",
                 "compiled/text.pyc",
                 "compiled/platforms.pyc",
                 "compiled/player.pyc",
                 "compiled/spritesheet.pyc",
                 "compiled/terrain.pyc",
                 "compiled/torches.pyc",
                 "compiled/funcs.pyc",
                 "compiled/game.pyc",
                 "compiled/menu.pyc",
                 "compiled/hud.pyc",
                 "compiled/saves.pyc",
                 "compiled/sounds.pyc",
                 "compiled/GIFImage.pyc",
                 "source/save_data.json"]

# All of the packages we don't want
excludes = ["OpenGL",
            "email",
            "html",
            "http",
            "multiprocessing",
            "numpy",
            "urllib",
            "xml",
            "socket"]

# The required packages
packages = ["pygame",
            "json",
            "os",
            "PIL",
            "logging"]

# Then finally set it up
cx_Freeze.setup(
    name="Stealth",
    options={
        "build_exe": {
            "packages": packages,
            "excludes": excludes,
            "include_files": include_files
        }
    },
    executables=executables
)

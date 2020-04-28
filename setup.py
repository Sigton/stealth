import cx_Freeze

# First of compile of the source files, since they
# take up less storage space when compiled
"""
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
"""

# Set up the executable
executables = [cx_Freeze.Executable(script="source/main.py",
                                    icon="source/src/resources/icon.ico",
                                    targetName="Stealth.exe")]

# All of the files that need to be included
include_files = ["source/src"]

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

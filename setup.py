from cx_Freeze import setup, Executable

executaveis = [
    Executable(
        script="main.py",
        icon="base/icone.ico",
        target_name="Dragon Escape.exe"
    )
]

setup(
    name="Dragon Escape",
    options={
        "build_exe": {
            "packages": ["pygame"],
            "include_files": ["base", "recursos"]
        }
    },
    executables=executaveis
)

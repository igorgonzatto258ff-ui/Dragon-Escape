# pip install cx_freeze
import cx_Freeze
executaveis = [ 
               cx_Freeze.Executable(
                   script="main.py", 
                   icon="assets/icone.ico",
                    target_name="Dragon Escape.exe"
                   ) ]
cx_Freeze.setup(
    name = "Dragon Escape",
    options={
        "build_exe":{
            "packages":["pygame"],
            "include_files":["assets","recursos"]
        }
    }, executables = executaveis
)

# python setup.py build
# python setup.py bdist_msi
import os
import cx_Freeze
os.environ['TCL_LIBRARY'] = "C:\\Users\\RistomattiPau\\AppData\\Local\\Programs\\Python\\Python37\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\RistomattiPau\\AppData\\Local\\Programs\\Python\\Python37\\tcl\\tk8.6"

base = None

executables = [cx_Freeze.Executable('f1_api_gui.py', base=base)]
packages = ['ergast_api','tkinter','matplotlib','idna','numpy.core._methods','numpy.lib.format']
included_files = ['tcl86t.dll','tk86t.dll']

cx_Freeze.setup(
    name = 'F1 API GUI',
    options={'build_exe': {'packages': packages,'include_files':included_files}},
    executables = executables
    )
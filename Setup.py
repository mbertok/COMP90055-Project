import sys
from cx_Freeze import setup,Executable
import packaging
import packaging.version
import packaging.specifiers
import packaging.requirements
import os

additional_mods = ['numpy.core._methods', 'mesa','numpy.lib.format','pkg_resources._vendor','appdirs', 'packaging.version','packaging.specifiers','packaging.requirements']
additional_packages = [ 'numpy', 'appdirs','networkx','atexit','secrets','secrets','scipy']
excludes=['scipy.spatial.cKDTree']

os.environ['TCL_LIBRARY'] = r'C:\Users\Marci\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Marci\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6'

setup(
    name="Agents",
    version="3.6",
    description="An agent based model to monitor epidemics",
    options={'build_exe': {'includes': additional_mods,'packages': additional_packages,'excludes':excludes
        #,'include_files': ["tcl86t.dll", "tk86t.dll"]

}},
    executables=[Executable("Start_Sim.py",base=None)]
    #executables=[Executable("Start_Sim.py",base="Win32GUI")]

)

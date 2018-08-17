from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile

class PythonToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False)
    depends_on('python')

    def install(self, spec, prefix):
        pyvers=str(self.spec['python'].version).split('.')
        pyver=pyvers[0]+'.'+pyvers[1]
        values={}
        values['VER']=self.spec.version
        values['PFX']=self.spec.prefix
        values['PYVER']=pyver
        fname='python.xml'
        contents = str("""<tool name="python" version="$VER">
  <lib name="python${PYVER}"/>
  <client>
    <environment name="PYTHON_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$PFX/lib"/>
    <environment name="INCLUDE" default="$PFX/include/python${PYVER}"/>
    <environment name="PYTHON_COMPILE" default="$PFX/lib/python${PYVER}/compileall.py"/>
  </client>
  <runtime name="PATH" value="$PFX/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$PFX/include/python${PYVER}" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="sockets"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)

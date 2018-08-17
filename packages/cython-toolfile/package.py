from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class CythonToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False)
    depends_on('cython')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['cython'].version
        values['PFX'] = self.spec['cyhton'].prefix
        fname = 'cython.xml'
        contents = str("""
<tool name="cython" version="${VER}">
  <client>
    <environment name="CYTHON_BASE" default="${PFX}"/>
  </client>
  <runtime name="PYTHONPATH" value="${PFX}/lib/python2.7/site-packages" type="path"/>
  <use name="python"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)

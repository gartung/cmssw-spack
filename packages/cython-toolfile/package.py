from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class CythonToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('cython')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['cython'].version
        values['PFX'] = spec['cyhton'].prefix
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
        write_scram_toolfile(contents, values, fname, prefix)

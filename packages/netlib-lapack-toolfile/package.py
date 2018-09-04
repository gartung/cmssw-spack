from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile

class NetlibLapackToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('lapack')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['lapack'].version
        values['PFX'] = spec['lapack'].prefix
        fname = 'lapack.xml'
        contents = str("""
<tool name="lapack" version="${VER}">
  <client>
    <environment name="LAPACK_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$LAPACK_BASE/lib64"/>
  </client>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

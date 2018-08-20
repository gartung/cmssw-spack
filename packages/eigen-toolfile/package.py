from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class EigenToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('eigen-cms')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['eigen-cms'].version
        values['PFX'] = spec['eigen-cms'].prefix
        fname = 'eigen3.xml'
        contents = str("""
<tool name="eigen" version="${VER}">
  <client>
    <environment name="EIGEN_BASE"   default="${PFX}"/>
    <environment name="INCLUDE"      default="$$EIGEN_BASE/include/eigen3"/>
  </client>
  <flags CPPDEFINES="EIGEN_DONT_PARALLELIZE"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

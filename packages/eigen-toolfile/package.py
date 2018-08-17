from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class EigenToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=True)
    depends_on('eigen')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['eigen'].version
        values['PFX'] = self.spec['eigen'].prefix
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
        write_scram_toolfile(contents, values, fname)

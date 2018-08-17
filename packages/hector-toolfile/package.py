from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class HectorToolfile(Package):

    version('1.0', '', expand=True)
    depends_on('hector')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['hector'].version
        values['PFX'] = self.spec['hector'].prefix
        fname = 'hector.xml'
        contents = str("""
<tool name="Hector" version="${VER}">
  <info url="http://www.fynu.ucl.ac.be/themes/he/ggamma/hector/"/>
  <lib name="Hector"/>
  <client>
    <environment name="HECTOR_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$HECTOR_BASE/lib"/>
    <environment name="INCLUDE" default="$$HECTOR_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)

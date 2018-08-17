from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class DcapToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False)
    depends_on('dcap')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['dcap'].version
        values['PFX'] = self.spec['dcap'].prefix
        fname = 'dcap.xml'
        contents = str("""
<tool name="dcap" version="${VER}">
  <lib name="dcap"/>
  <client>
    <environment name="DCAP_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$DCAP_BASE/lib"/>
    <environment name="INCLUDE" default="$$DCAP_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)


from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile



class HeppdtToolfile(Package):

    depends_on('heppdt')

    def install(self,spec,prefix):
        values = {}
        values['VER'] = self.spec['heppdt'].version
        values['PFX'] = self.spec['heppdt'].prefix

        fname = 'heppdt.xml'
        contents = str("""
<tool name="heppdt" version="${VER}">
  <lib name="HepPDT"/>
  <lib name="HepPID"/>
  <client>
    <environment name="HEPPDT_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$HEPPDT_BASE/lib"/>
    <environment name="INCLUDE" default="$$HEPPDT_BASE/include"/>
  </client>
  <runtime name="HEPPDT_PARAM_PATH" value="$$HEPPDT_BASE"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <flags SKIP_TOOL_SYMLINKS="1"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)

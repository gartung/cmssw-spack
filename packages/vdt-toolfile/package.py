from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class VdtToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('vdt')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['vdt'].version
        values['PFX'] = self.spec['vdt'].prefix

        fname = 'vdt_headers.xml'
        contents = str("""<tool name="vdt_headers" version="$VER">
  <client>
    <environment name="VDT_HEADERS_BASE" default="$PFX"/>
    <environment name="INCLUDE" default="$$VDT_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")

        write_scram_toolfile(contents, values, fname, prefix)

        fname = 'vdt.xml'
        contents = str("""<tool name="vdt" version="$VER">
  <lib name="vdt"/>
  <use name="vdt_headers"/>
  <client>
    <environment name="VDT_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$VDT_BASE/lib"/>
  </client>
</tool>""")

        write_scram_toolfile(contents, values, fname, prefix)

from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class JimmyToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('jimmy')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['jimmy'].version
        values['PFX'] = spec['jimmy'].prefix
        fname = 'jimmy.xml'
        contents = str("""
<tool name="jimmy" version="${VER}">
  <lib name="jimmy"/>
  <client>
    <environment name="JIMMY_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$JIMMY_BASE/lib"/>
  </client>
  <use name="f77compiler"/>
  <use name="herwig"/>
  <use name="jimmy_headers"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

        fname = 'jimmy_headers.xml'
        contents = str("""
<tool name="jimmy_headers" version="${VER}">
  <client>
    <environment name="JIMMY_HEADERS_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$JIMMY_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

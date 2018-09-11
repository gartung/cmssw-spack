from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile



class TauolaToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('tauola@27.121.5')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['tauola'].version
        values['PFX'] = spec['tauola'].prefix

        fname = 'tauola.xml'
        contents = str("""
<tool name="tauola" version="${VER}">
  <lib name="pretauola"/>
  <lib name="tauola"/>
  <client>
    <environment name="TAUOLA_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$TAUOLA_BASE/lib"/>
  </client>
  <use name="f77compiler"/>
  <use name="tauola_headers"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname, prefix)

        fname = 'tauola_headers.xml'
        contents = str("""
<tool name="tauola_headers" version="${VER}">
  <client>
    <environment name="TAUOLA_HEADERS_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$TAUOLA_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname, prefix)

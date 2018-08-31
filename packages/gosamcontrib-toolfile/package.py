from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class GosamcontribToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('gosamcontrib')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['gosamcontrib'].version
        values['PFX'] = spec['gosamcontrib'].prefix

        fname = 'gosamcontrib.xml'
        contents = str("""
<tool name="gosamcontrib" version="$VER">
  <client>
    <environment name="GOSAMCONTRIB_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$GOSAMCONTRIB_BASE/lib"/>
    <environment name="INCLUDE" default="$$GOSAMCONTRIB_BASE/include"/>
  </client>
  <runtime name="GOSAMCONTRIB_PATH" value="$$GOSAMCONTRIB_BASE" type="path"/>
  <runtime name="ROOT_PATH" value="$$GOSAMCONTRIB_BASE" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
</tool>

""")

        write_scram_toolfile(contents, values, fname, prefix)

from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class GblToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('gbl')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['gbl'].version
        values['PFX'] = spec['gbl'].prefix

        fname = 'gbl.xml'
        contents = str("""<tool name="gbl" version="$VER">
  <lib name="GBL"/>
  <client>
    <environment name="GBL_BASE" default="$PFX"/>
    <environment name="INCLUDE"        default="$$GBL_BASE/include"/>
    <environment name="LIBDIR"        default="$$GBL_BASE/lib"/>
  </client>
  <use name="eigen"/>
</tool>""")

        write_scram_toolfile(contents, values, fname, prefix)

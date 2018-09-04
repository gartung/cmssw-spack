from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class DireToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('dire')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['dire'].version
        values['PFX'] = spec['dire'].prefix

        fname = 'dire.xml'
        contents = str("""
<tool name="dire" version="$VER">
  <lib name="dire"/>
  <client>
    <environment name="DIRE_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$DIRE_BASE/lib"/>
    <environment name="INCLUDE" default="$$DIRE_BASE/include"/>
    <environment name="BINDIR" default="$$DIRE_BASE/bin"/>
  </client>
  <runtime name="PATH" default="$$BINDIR" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="pythia8"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname, prefix)

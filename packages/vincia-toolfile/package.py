from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class VinciaToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('vincia@2.2.01')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['vincia'].version
        values['PFX'] = spec['vincia'].prefix

        fname = 'vincia.xml'
        contents = str("""
<tool name="vincia" version="$VER">
  <lib name="vincia"/>
  <lib name="VinciaMG4"/>
  <lib name="VinciaMG5"/>
  <client>
    <environment name="VINCIA_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$VINCIA_BASE/lib"/>
    <environment name="INCLUDE" default="$$VINCIA_BASE/include"/>
  </client>
  <runtime name="VINCIADATA" value="$$VINCIA_BASE/share/Vincia/xmldoc"/>
  <use name="root_cxxdefaults"/>
  <use name="pythia8"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname, prefix)

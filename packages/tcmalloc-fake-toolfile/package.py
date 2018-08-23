from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class TcmallocFakeToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('tcmalloc-fake')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['tcmalloc-fake'].version
        values['PFX'] = spec['tcmalloc-fake'].prefix

        fname = 'tcmalloc_minimal.xml'
        contents = str("""<tool name="tcmalloc_minimal" version="$VER">
  <lib name="tcmalloc_minimal"/>
  <client>
    <environment name="TCMALLOC_MINIMAL_BASE" default="$PFX"/>
    <environment name="LIBDIR"                default="$$TCMALLOC_MINIMAL_BASE/lib"/>
  </client>
</tool>""")

        write_scram_toolfile(contents, values, fname, prefix)

        fname = 'tcmalloc.xml'
        contents = str("""<tool name="tcmalloc" version="$VER">
  <lib name="tcmalloc"/>
  <client>
    <environment name="TCMALLOC_BASE" default="$PFX"/>
    <environment name="LIBDIR"        default="$$TCMALLOC_BASE/lib"/>
  </client>
</tool>""")

        write_scram_toolfile(contents, values, fname, prefix)

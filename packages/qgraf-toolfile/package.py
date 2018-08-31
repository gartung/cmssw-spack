from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class QgrafToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('qgraf')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['qgraf'].version
        values['PFX'] = spec['qgraf'].prefix

        fname = 'qgraf.xml'
        contents = str("""
<tool name="qgraf" version="$VER">
  <client>
    <environment name="QGRAF_BASE" default="$PFX"/>
    <environment name="BINDIR" default="$$QGRAF_BASE/bin"/>
  </client>
  <runtime name="PATH" default="$$BINDIR" type="path"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname, prefix)

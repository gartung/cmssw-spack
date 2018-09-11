from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class GmakeToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('gmake@4.2.1')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['gmake'].version
        values['PFX'] = spec['gmake'].prefix
        fname = 'gmake.xml'
        contents = str("""<tool name="gmake" version="$VER">
  <client>
    <environment name="MAKE_BASE" default="$PFX"/>
  </client>
  <runtime name="PATH" value="$$MAKE_BASE/bin" type="path"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

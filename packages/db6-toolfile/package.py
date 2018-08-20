from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Db6Toolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('berkely-db')

    def install(self,spec,prefix):
        values = {}
        values['VER'] = spec['berkley-db'].version
        values['PFX'] = spec['berkley-db'].prefix

        fname = 'db6.xml'
        contents = str("""
<tool name="db6" version="${VER}">
  <lib name="db"/>
  <client>
    <environment name="DB6_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$DB6_BASE/lib"/>
    <environment name="INCLUDE" default="$$DB6_BASE/include"/>
    <environment name="BINDIR" default="$$DB6_BASE/bin"/>
  </client>
  <runtime name="PATH" value="$$BINDIR" type="path"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

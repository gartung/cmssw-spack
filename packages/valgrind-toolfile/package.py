from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class ValgrindToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('valgrind')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['valgrind'].version
        values['PFX'] = spec['valgrind'].prefix

        fname = 'valgrind.xml'
        contents = str("""
<tool name="valgrind" version="${VER}">
  <client>
    <environment name="VALGRIND_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$VALGRIND_BASE/include"/>
  </client>
  <runtime name="PATH" value="$$VALGRIND_BASE/bin" type="path"/>
  <runtime name="VALGRIND_LIB" value="$$VALGRIND_BASE/lib/valgrind"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname, prefix)

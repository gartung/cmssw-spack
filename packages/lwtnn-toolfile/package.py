from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class LwtnnToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('lwtnn')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'lwtnn.xml'
        contents = str("""
<tool name="lwtnn" version="${VER}">
  <info url="https://github.com/lwtnn/lwtnn"/>
  <lib name="lwtnn"/>
  <client>
    <environment name="LWTNN_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$LWTNN_BASE/lib"/>
    <environment name="INCLUDE" default="$$LWTNN_BASE/include"/>
  </client>
  <runtime name="PATH" value="$$LWTNN_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="eigen"/>
  <use name="boost_system"/>  
  <flags SKIP_TOOL_SYMLINKS="1"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

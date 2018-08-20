from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class KtjetToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('ktjet')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['ktjet'].version
        values['PFX'] = spec['ktjet'].prefix

        fname = 'ktjet.xml'
        contents = str("""
<tool name="ktjet" version="${VER}">
  <info url="http://hepforge.cedar.ac.uk/ktjet"/>
  <lib name="KtEvent"/>
  <client>
    <environment name="KTJET_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$KTJET_BASE/lib"/>
    <environment name="INCLUDE" default="$$KTJET_BASE/include"/>
  </client>
  <flags cppdefines="KTDOUBLEPRECISION"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <flags SKIP_TOOL_SYMLINKS="1"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class MeschachToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)

    depends_on('meschach')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix
        fname = 'meschach.xml'
        contents = str("""<tool name="meschach" version="$VER">
  <info url="http://www.meschach.com"/>
  <lib name="meschach"/>
  <client>
    <environment name="MESCHACH_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$MESCHACH_BASE/lib"/>
    <environment name="INCLUDE" default="$$MESCHACH_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class UtmToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('utm')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'utm.xml'
        contents = str("""
<tool name="utm" version="${VER}">
  <lib name="tmeventsetup"/>
  <lib name="tmtable"/>
  <lib name="tmxsd"/>
  <lib name="tmgrammar"/>
  <lib name="tmutil"/>
  <client>
    <environment name="UTM_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$UTM_BASE/lib"/>
    <environment name="INCLUDE" default="$$UTM_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <runtime name="UTM_XSD_DIR" value="$$UTM_BASE"/>
  <use name="root_cxxdefaults"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname, prefix)

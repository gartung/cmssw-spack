from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class YodaToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('yoda')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'yoda.xml'
        contents = str("""
<tool name="yoda" version="${VER}">
  <lib name="YODA"/>
  <client>
    <environment name="YODA_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$YODA_BASE/lib"/>
    <environment name="INCLUDE" default="$$YODA_BASE/include"/>
  </client>
  <use name="root_cxxdefaults"/>
  <runtime name="PATH"       value="$$YODA_BASE/bin" type="path"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

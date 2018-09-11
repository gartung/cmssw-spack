from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class LibhepmlToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('libhepml@0.2.1')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['libhepml'].version
        values['PFX'] = spec['libhepml'].prefix

        fname = 'libhepml.xml'
        contents = str("""
<tool name="libhepml" version="${VER}">
  <lib name="hepml"/>
  <client>
    <environment name="LIBHEPML_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$LIBHEPML_BASE/lib"/>
    <environment name="INCLUDE" default="$$LIBHEPML_BASE/interface"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

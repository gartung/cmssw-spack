from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Libxml2Toolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('libxml2')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['libxml2'].version
        values['PFX'] = spec['libxml2'].prefix

        fname = 'libxml2.xml'
        contents = str("""<tool name="libxml2" version="$VER">
  <info url="http://xmlsoft.org/"/>
  <lib name="xml2"/>
  <client>
    <environment name="LIBXML2_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$LIBXML2_BASE/lib"/>
    <environment name="INCLUDE" default="$$LIBXML2_BASE/include/libxml2"/>
  </client>
  <runtime name="PATH" value="$$LIBXML2_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

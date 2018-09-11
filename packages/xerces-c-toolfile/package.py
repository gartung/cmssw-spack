from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class XercesCToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('xerces-c')

    def install(self,spec,prefix):
        values = {}
        values['VER'] = spec['xerces-c'].version
        values['PFX'] = spec['xerces-c'].prefix
        fname = 'xerces-c.xml'
        contents = str("""<tool name="xerces-c" version="$VER">
  <info url="http://xml.apache.org/xerces-c/"/>
  <lib name="xerces-c"/>
  <client>
    <environment name="XERCES_C_BASE" default="$PFX"/>
    <environment name="INCLUDE" default="$$XERCES_C_BASE/include"/>
    <environment name="LIBDIR" default="$$XERCES_C_BASE/lib"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

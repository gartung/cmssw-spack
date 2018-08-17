from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class XercesCToolfile(AutotoolsPackage):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=True)
    depends_on('xerces-c')

    def install(self,spec,prefix):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix
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
        write_scram_toolfile(contents, values, fname)

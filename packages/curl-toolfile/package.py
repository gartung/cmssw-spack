from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class CurlToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False)
    depends_on('curl')
    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix
        fname = 'curl.xml'
        contents = str("""
<tool name="curl" version="${VER}">
  <lib name="curl"/>
  <client>
    <environment name="CURL_BASE" default="${PFX}"/>
    <environment name="INCLUDE"      default="$$CURL_BASE/include"/>
    <environment name="LIBDIR"       default="$$CURL_BASE/lib"/>
  </client>
  <runtime name="PATH" value="$$CURL_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <flags SKIP_TOOL_SYMLINKS="1"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)

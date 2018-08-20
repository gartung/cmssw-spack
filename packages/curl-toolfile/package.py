from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class CurlToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('curl')
    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['curl'].version
        values['PFX'] = spec['curl'].prefix
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
        write_scram_toolfile(contents, values, fname, prefix)

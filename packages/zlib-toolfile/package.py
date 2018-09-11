from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class ZlibToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('zlib@1.2.11')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['zlib'].version
        values['PFX'] = self.spec['zlib'].prefix
        fname = 'zlib.xml'
        contents = str("""
<tool name="zlib" version="$VER">
  <lib name="z"/>
  <client>
    <environment name="ZLIB_BASE" default="$PFX"/>
    <environment name="INCLUDE" default="$$ZLIB_BASE/include"/>
    <environment name="LIBDIR" default="$$ZLIB_BASE/lib"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

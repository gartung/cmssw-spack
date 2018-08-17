from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class ZlibToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0.0', '', expand=False)
    depends_on('zlib')

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
        write_scram_toolfile(contents, values, fname)

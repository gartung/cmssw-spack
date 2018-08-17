from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class FreetypeToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    depends_on('freetype')
    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['freetype'].version
        values['PFX'] = self.spec['freetype'].prefix
        fname = 'freetype.xml'
        contents = str("""
<tool name="freetype" version="${VER}">
  <lib name="freetype-cms"/>
  <client>
    <environment name="FREETYPE_BASE" default="${PFX}"/>
    <environment name="INCLUDE"      default="$$FREETYPE_BASE/include"/>
    <environment name="LIBDIR"       default="$$FREETYPE_BASE/lib"/>
  </client>
  <runtime name="PATH" value="$$FREETYPE_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)

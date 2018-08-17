from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class GmakeToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=True)
    depends_on('gmake')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['gmake'].version
        values['PFX'] = self.spec['gmake'].prefix
        fname = 'gmake.xml'
        contents = str("""<tool name="gmake" version="$VER">
  <client>
    <environment name="MAKE_BASE" default="$PFX"/>
  </client>
  <runtime name="PATH" value="$$MAKE_BASE/bin" type="path"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)

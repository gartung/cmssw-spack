from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class ExpatToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False) 
    depends_on('expat')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['expat'].version
        values['PFX'] = self.spec['expat'].prefix
        fname = 'expat.xml'
        contents = str("""<tool name="expat" version="$VER">
  <lib name="expat"/>
  <client>
    <environment name="EXPAT_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$EXPAT_BASE/lib"/>
    <environment name="INCLUDE" default="$$EXPAT_BASE/include"/>
    <environment name="BINDIR" default="$$EXPAT_BASE/bin"/>
  </client>
  <runtime name="PATH" value="$$BINDIR" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")

        write_scram_toolfile(contents, values, fname)

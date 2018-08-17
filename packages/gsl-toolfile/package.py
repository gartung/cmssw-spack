from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class GslToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False)
    depends_on('gsl')

    def install(self,spec,prefix):
        values = {}
        values['VER'] = self.spec['gsl'].version
        values['PFX'] = self.spec['gsl'].prefix
        fname = 'gsl.xml'
        contents = str("""<tool name="gsl" version="$VER">
  <info url="http://www.gnu.org/software/gsl/gsl.html"/>
  <lib name="gsl"/>
  <lib name="gslcblas"/>
  <client>
    <environment name="GSL_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$GSL_BASE/lib"/>
    <environment name="INCLUDE" default="$$GSL_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)

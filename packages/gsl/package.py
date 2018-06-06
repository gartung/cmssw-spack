from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile



class Gsl(AutotoolsPackage):
    """The GNU Scientific Library (GSL) is a numerical library for C and C++
    programmers. It is free software under the GNU General Public License. The
    library provides a wide range of mathematical routines such as random
    number generators, special functions and least-squares fitting. There are
    over 1000 functions in total with an extensive test suite."""

    homepage = "http://www.gnu.org/software/gsl"
    url = "http://mirror.switch.ch/ftp/mirror/gnu/gsl/gsl-2.3.tar.gz"

    version('2.4',   'dba736f15404807834dc1c7b93e83b92')
    version('2.3',   '905fcbbb97bc552d1037e34d200931a0')
    version('2.2.1', '3d90650b7cfe0a6f4b29c2d7b0f86458')
    version('2.1',   'd8f70abafd3e9f0bae03c52d1f4e8de5')
    version('2.0',   'ae44cdfed78ece40e73411b63a78c375')
    version('1.16',  'e49a664db13d81c968415cd53f62bc8b')

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

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

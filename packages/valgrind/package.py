from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Valgrind(AutotoolsPackage):
    """An instrumentation framework for building dynamic analysis.

    There are Valgrind tools that can automatically detect many memory
    management and threading bugs, and profile your programs in
    detail. You can also use Valgrind to build new tools.

    Valgrind is Open Source / Free Software, and is freely available
    under the GNU General Public License, version 2.

    """
    homepage = "http://valgrind.org/"
    url = "http://valgrind.org/downloads/valgrind-3.11.0.tar.bz2"

    version('3.12.0', '6eb03c0c10ea917013a7622e483d61bb')
    version('3.11.0', '4ea62074da73ae82e0162d6550d3f129')
    version('3.10.1', '60ddae962bc79e7c95cfc4667245707f')
    version('3.10.0', '7c311a72a20388aceced1aa5573ce970')
    version('develop', svn='svn://svn.valgrind.org/valgrind/trunk')

    variant('mpi', default=False,
            description='Activates MPI support for valgrind')
    variant('boost', default=False,
            description='Activates boost support for valgrind')

    depends_on('mpi', when='+mpi')
    depends_on('boost', when='+boost')

    depends_on("autoconf", type='build', when='@develop')
    depends_on("automake", type='build', when='@develop')
    depends_on("libtool", type='build', when='@develop')

    def configure_args(self):
        spec = self.spec
        options = []
        if not (spec.satisfies('%clang') and sys.platform == 'darwin'):
            # Otherwise with (Apple's) clang there is a linker error:
            # clang: error: unknown argument: '-static-libubsan'
            options.append('--enable-ubsan')

        return options


    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'valgrind.xml'
        contents = str("""
<tool name="valgrind" version="${VER}">
  <client>
    <environment name="VALGRIND_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$VALGRIND_BASE/include"/>
  </client>
  <runtime name="PATH" value="$$VALGRIND_BASE/bin" type="path"/>
  <runtime name="VALGRIND_LIB" value="$$VALGRIND_BASE/lib/valgrind"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)

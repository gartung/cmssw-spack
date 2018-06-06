from spack import *
from spack import architecture
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Sqlite(AutotoolsPackage):
    """SQLite3 is an SQL database engine in a C library. Programs that
       link the SQLite3 library can have SQL database access without
       running a separate RDBMS process.
    """
    homepage = "www.sqlite.org"

    version('3.20.0', 'e262a28b73cc330e7e83520c8ce14e4d',
            url='https://www.sqlite.org/2017/sqlite-autoconf-3200000.tar.gz')
    version('3.18.0', 'a6687a8ae1f66abc8df739aeadecfd0c',
            url='https://www.sqlite.org/2017/sqlite-autoconf-3180000.tar.gz')
    version('3.16.02', '0259d52be88f085d104c6d2aaa8349ac',
            url='https://www.sqlite.org/2016/sqlite-autoconf-3150100.tar.gz',
            preferred=True)
    version('3.8.10.2', 'a18bfc015cd49a1e7a961b7b77bc3b37',
            url='https://www.sqlite.org/2015/sqlite-autoconf-3081002.tar.gz')
    version('3.8.5', '0544ef6d7afd8ca797935ccc2685a9ed',
            url='https://www.sqlite.org/2014/sqlite-autoconf-3080500.tar.gz')

    depends_on('readline')

    # On some platforms (e.g., PPC) the include chain includes termios.h which
    # defines a macro B0. Sqlite has a shell.c source file that declares a
    # variable named B0 and will fail to compile when the macro is found. The
    # following patch undefines the macro in shell.c
    patch('sqlite_b0.patch', when='@3.18.0')

    def get_arch(self):
        arch = architecture.Arch()
        arch.platform = architecture.platform()
        return str(arch.platform.target('default_target'))

    def configure_args(self):
        args = []

        if self.get_arch() == 'ppc64le':
            args.append('--build=powerpc64le-redhat-linux-gnu')

        return args

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'sqlite.xml'
        contents = str("""<tool name="sqlite" version="$VER">
  <lib name="sqlite3"/>
  <client>
    <environment name="SQLITE_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$SQLITE_BASE/lib"/>
    <environment name="BINDIR" default="$$SQLITE_BASE/bin"/>
    <environment name="INCLUDE" default="$$SQLITE_BASE/include"/>
  </client>
  <runtime name="PATH" value="$$BINDIR" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")

        write_scram_toolfile(contents, values, fname)

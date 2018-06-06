from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile



class Gmake(AutotoolsPackage):
    """GNU Make is a tool which controls the generation of executables and
    other non-source files of a program from the program's source files."""

    homepage = "https://www.gnu.org/software/make/"
    url = "https://ftp.gnu.org/gnu/make/make-4.2.1.tar.gz"

    version('4.2.1', '7d0dcb6c474b258aab4d54098f2cf5a7')
    version('4.0',   'b5e558f981326d9ca1bfdb841640721a')

    variant('guile', default=False,
            description='Support GNU Guile for embedded scripting')

    depends_on('guile', when='+guile')

    build_directory = 'spack-build'

    def configure_args(self):
        args = []

        if '+guile' in self.spec:
            args.append('--with-guile')
        else:
            args.append('--without-guile')

        return args

    @run_after('install')
    def symlink_gmake(self):
        with working_dir(self.prefix.bin):
            symlink('make', 'gmake')

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'gmake.xml'
        contents = str("""<tool name="gmake" version="$VER">
  <client>
    <environment name="MAKE_BASE" default="$PFX"/>
  </client>
  <runtime name="PATH" value="$$MAKE_BASE/bin" type="path"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)

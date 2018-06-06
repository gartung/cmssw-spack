from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Dcap(AutotoolsPackage):
    homepage = "http://www.example.com"
    url      = "https://github.com/cms-externals/dcap/archive/2.47.8.tar.gz"

    version('2.47.8', '8dfa5b3d665a7c950050b05576c59d8e')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    depends_on('zlib')

    def autoreconf(self, spec, prefix):
        filter_file(r'library_includedir.*', 
                   'library_includedir=$(includedir)',
                   'src/Makefile.am')
        mkdirp('config')
        aclocal('-I', 'config')
        autoheader()
        libtoolize('--automake')
        automake('--add-missing', '--copy', '--foreign')
        autoconf()

    def configure_args(self):
        args = ['CFLAGS=-I%s' % self.spec['zlib'].prefix.include,
                'LDFLAGS=-L%s' % self.spec['zlib'].prefix.lib ]
        return args

    def install(self, spec, prefix):
        make('-C', 'src')
        make('-C', 'src', 'install')

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'dcap.xml'
        contents = str("""
<tool name="dcap" version="${VER}">
  <lib name="dcap"/>
  <client>
    <environment name="DCAP_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$DCAP_BASE/lib"/>
    <environment name="INCLUDE" default="$$DCAP_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)


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

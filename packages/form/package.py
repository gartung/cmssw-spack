from spack import *


class Form(AutotoolsPackage):
    homepage = "http://www.example.com"
    url      = "https://gosam.hepforge.org/gosam-installer/form-4.1.033e.tar.gz"

    version('4.1.033e', sha256='b182e10f9969238daea453c14ada9989a4818d23aad8855a8eb5968a231f545c')


    def configure_args(self):
        args = ['--enable-shared', '--disable-static','--without-gmp', 'CXXFLAGS=-fpermissive']
        return args

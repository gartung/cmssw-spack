from spack import *


class Vincia(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "http://www.example.com"
    url      = "https://www.hepforge.org/archive/vincia/vincia-2.2.01.tgz"

    version('2.2.01', sha256='4c93014cdb3813e10e36d8df494bda75366b81c6a985c729dd15e5089762ec20')
    version('2.2.02', sha256='4c93014cdb3813e10e36d8df494bda75366b81c6a985c729dd15e5089762ec20')

    depends_on('pythia8')

    def configure_args(self):
        args = ['--with-pythia8=%s'%self.spec['pythia8'].prefix
                ,'--enable-shared']
        return args

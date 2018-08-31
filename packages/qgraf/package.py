from spack import *


class Qgraf(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://gosam.hepforge.org/gosam-installer/qgraf-3.1.4.tgz"

    version('3.1.4', sha256='b6f827a654124b368ea17cd391a78a49cda70e192e1c1c22e8e83142b07809dd')

    def install(self, spec, prefix):
        FC=which(spack_f77)
        FC('qgraf-3.1.4.f','-o','qgraf','-O2')
        mkdirp(prefix.bin)
        install('qgraf', prefix.bin)

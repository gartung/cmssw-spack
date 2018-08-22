from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Ktjet(AutotoolsPackage):
    homepage = "http://www.example.com"
    url      = "http://www.hepforge.org/archive/ktjet/KtJet-1.0.6.tar.gz"

    version('1.06', '44294e965734da8844395c446a813d7e')

    depends_on('clhep')

    patch('ktjet-1.0.6-nobanner.patch')

    def configure_args(self):

        args = ['--with-clhep=%s'%self.spec['clhep'].prefix,
                'CPPFLAGS=-DKTDOUBLEPRECISION -fPIC']
        return args


from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Photospp(Package):
    homepage = "http://www.example.com"
    url = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/photos++/photos++-3.61-src.tgz"

    version('3.61', 'b5519bb2b22a51710f67014704f6795a')

    depends_on('hepmc')

    def install(self, spec, prefix):
        with working_dir(str(spec.version)):
            configure('--prefix=%s' % prefix, '--with-hepmc=%s' %
                      spec['hepmc'].prefix)
            make()
            make('install')

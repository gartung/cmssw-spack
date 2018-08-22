from spack import *
import distutils.dir_util as du
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Pythia6(Package):
    """PYTHIA is a program for the generation of high-energy physics events,
    i.e. for the description of collisions at high energies between elementary
    particles such as e+, e-, p and pbar in various combinations."""

    homepage = "https://pythia6.hepforge.org/"
    url = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/pythia6/pythia6-426-src.tgz"

    version('426', '4dd75f551b7660c35f817c063abd74ca91b70259c0987905a06ebb2d21bcdf26')

    def install(self, spec, prefix):
        with working_dir(self.version.string):
            configure('--with-hepevt=4000')
            make()
            make('install')
            du.copy_tree('lib',prefix.lib)
            du.copy_tree('include',prefix.include)

    def url_for_version(self,version):
        url='http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/pythia6/pythia6-426-src.tgz'%self.version
        return url


from spack import *
import glob
import sys,os

class Geant4G4radioactivedecay(Package):

    url = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc7_amd64_gcc700/external/geant4-G4RadioactiveDecay/5.2/G4RadioactiveDecay.5.2.tar.gz"

    version('5.2', 'e035ed77e12be3a69c2d32806d1b5cde')

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data',
                                 os.path.basename(self.stage.source_path))
        install_tree(self.stage.source_path, install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc7_amd64_gcc700/external/geant4-G4RadioactiveDecay/%s/G4RadioactiveDecay.%s.tar.gz" % (version,version))

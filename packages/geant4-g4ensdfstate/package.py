from spack import *
import glob
import sys,os

class Geant4G4ensdfstate(Package):

    url = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc7_amd64_gcc700/external/geant4-G4ENSDFSTATE/2.2/G4ENSDFSTATE.2.2.tar.gz"

    version('2.2', '495439cf600225753d7bd99825e5c6bc')

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data',
                                 os.path.basename(self.stage.source_path))
        install_tree(self.stage.source_path, install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc7_amd64_gcc700/external/geant4-G4ENSDFSTATE/%s/G4ENSDFSTATE.%s.tar.gz" % (version,version)

from spack import *
import glob
import sys,os

class Geant4G4photonevaporation(Package):

    url = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc7_amd64_gcc700/external/geant4-G4PhotonEvaporation/5.2/G4PhotonEvaporation.5.2.tar.gz"

    version('5.2', '37c5dea9614a07885050350d071a6973')

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data',
                                 os.path.basename(self.stage.source_path))
        install_tree(self.stage.source_path, install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc7_amd64_gcc700/external/geant4-G4PhotonEvaporation/%s/G4PhotonEvaporation.%s.tar.gz" % (version,version))


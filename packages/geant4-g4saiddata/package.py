from spack import *
import sys,os

class Geant4G4saiddata(Package):

    url = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc7_amd64_gcc700/external/geant4-G4SAIDDATA/1.1/G4SAIDDATA.1.1.tar.gz"

    version('1.1', 'd88a31218fdf28455e5c5a3609f7216f')

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data',
                                 os.path.basename(self.stage.source_path))
        install_tree(self.stage.source_path, install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc7_amd64_gcc700/external/geant4-G4SAIDDATA/%s/G4SAIDDATA.%s.tar.gz" % (version,version))


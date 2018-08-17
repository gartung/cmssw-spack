from spack import *
import glob
import sys,os

class Geant4G4abla(Package):

    url = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc7_amd64_gcc700/external/geant4-G4ABLA/3.0/G4ABLA.3.0.tar.gz"

    version('3.0', 'd7049166ef74a592cb97df0ed4b757bd')

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data',
                                 os.path.basename(self.stage.source_path))
        install_tree(self.stage.source_path, install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc7_amd64_gcc700/external/geant4-G4ABLA/%s/G4ABLA.%s.tar.gz" % (version,version))

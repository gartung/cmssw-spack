from spack import *
import glob
import sys,os

class Geant4G4neutronsxs(Package):

    url = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc7_amd64_gcc700/external/geant4-G4NEUTRONXS/1.4/G4NEUTRONXS.1.4.tar.gz"

    version('1.4', '665a12771267e3b31a08c622ba1238a7')

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data',
                                 os.path.basename(self.stage.source_path))
        install_tree(self.stage.source_path, install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc7_amd64_gcc700/external/geant4-G4NEUTRONXS/%s/G4NEUTRONXS.%s.tar.gz" % (version,version))

from spack import *
import glob
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile




class Geant4G4photonevaporation(Package):


    homepage = "http://www.example.com"
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

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PREFIX'] = self.spec.prefix.share + '/data'

        fname = 'geant4data_g4photonevaporation.xml'
        contents = str("""
<tool name="geant4data_g4photonevaporation" version="${VER}">
  <client>
    <environment name="GEANT4DATA_G4PhotonEvaporation" default="${PREFIX}"/>
  </client>
  <runtime name="G4LEVELGAMMADATA" value="${PREFIX}/PhotonEvaporation${VER}" type="path"/>
</tool>
""")


        write_scram_toolfile(contents, values, fname)

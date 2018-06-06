from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile




class Geant4G4saiddata(Package):


    homepage = "http://www.example.com"
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

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PREFIX'] = self.spec.prefix.share + '/data'

        fname = 'geant4data_g4saiddata.xml'
        contents = str("""
<tool name="geant4data_g4saiddata" version="${VER}">
  <client>
    <environment name="GEANT4DATA_G4SAIDDATA" default="${PREFIX}"/>
  </client>
  <runtime name="G4SAIDXSDATA" value="${PREFIX}/G4SAIDDATA${VER}" type="path"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)

from spack import *
import glob
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Geant4G4emlow(Package):


    homepage = "http://www.example.com"
    url = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc7_amd64_gcc700/external/geant4-G4EMLOW/7.3/G4EMLOW.7.3.tar.gz"

    version('7.3', '0446e7f53af993343956e5d3900157b8')

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data',
                                 os.path.basename(self.stage.source_path))
        install_tree(self.stage.source_path, install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc7_amd64_gcc700/external/geant4-G4EMLOW/%s/G4EMLOW.%s.tar.gz" % (version,version))

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PREFIX'] = self.spec.prefix.share + '/data'

        fname = 'geant4_g4emlow.xml'
        contents = str("""
<tool name="geant4data_g4emlow" version="${VER}">
  <client>
    <environment name="GEANT4DATA_G4EMLOW" default="${PREFIX}"/>
  </client>
  <runtime name="G4LEDATA" value="${PREFIX}/G4EMLOW${VER}" type="path"/>
</tool>
""")


        write_scram_toolfile(contents, values, fname)

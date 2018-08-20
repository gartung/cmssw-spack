from spack import *
import glob
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Geant4G4ablaToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('geant4-g4abla')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['geant4-g4abla'].version
        values['PREFIX'] = spec['geant4-g4abla'].prefix.share + '/data'
        fname = 'geant4data_g4abla.xml'
        contents = str("""
<tool name="geant4data_g4abla" version="${VER}">
  <client>
    <environment name="GEANT4DATA_G4ABLA" default="${PREFIX}"/>
  </client>
  <runtime name="G4ABLADATA" value="${PREFIX}/G4ABLA${VER}" type="path"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Geant4G4emlowToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False)
    depends_on('geant4-g4emlow')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['geant4-g4emlow'].version
        values['PREFIX'] = self.spec['geant4-g4emlow'].prefix.share + '/data'
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

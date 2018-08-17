from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Geant4G4ensdfstateToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False)
    depends_on('geant4-g4ensdfstate')
        
    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['geant4-g4ensdfstate'].version
        values['PREFIX'] = self.spec['geant4-g4ensdfstate'].prefix.share + '/data'
        fname = 'geant4data_g4ensdfstate.xml'
        contents = str("""
<tool name="geant4data_g4ensdfstate" version="${VER}">
  <client>
    <environment name="GEANT4DATA_G4ENSDFSTATE" default="${PREFIX}"/>
  </client>
  <runtime name="G4ENSDFSTATEDATA" value="${PREFIX}/G4ENSDFSTATE${VER}" type="path"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)

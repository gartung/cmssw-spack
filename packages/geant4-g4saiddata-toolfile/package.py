from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Geant4G4saiddataToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False)
    depends_on('geant4-g4saiddata')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['geant4-g4saiddata'].version
        values['PREFIX'] = self.spec['geant4-g4saiddata'].prefix.share + '/data'
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

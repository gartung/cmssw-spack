from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Geant4G4neutronsxsToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False)
    depends_on('geant4-g4neutronsxs')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['geant4-g4neutronsxs'].version
        values['PREFIX'] = self.spec['geant4-g4neutronsxs'].prefix.share + '/data'
        fname = 'geant4data_g4neutronsxs.xml'
        contents = str("""
<tool name="geant4data_g4neutronsxs" version="${VER}">
  <client>
    <environment name="GEANT4DATA_G4NEUTRONSXS" default="${PREFIX}"/>
  </client>
  <runtime name="G4NEUTRONXSDATA" value="${PREFIX}/G4NEUTRONXS${VER}" type="path"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)

from spack import *
import glob
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Geant4G4radioactivedecayToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False)
    depends_on('geant4-g4radioactivedecay')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['geant4-g4radioactivedecay'].version
        values['PREFIX'] = self.spec['geant4-g4radioactivedecay'].prefix.share + '/data'
        fname = 'geant4data_g4radioactivedecay.xml'
        contents = str("""
<tool name="geant4data_g4radioactivedecay" version="${VER}">
  <client>
    <environment name="GEANT4DATA_G4RadioactiveDecay" default="${PREFIX}"/>
  </client>
  <runtime name="G4RADIOACTIVEDATA" value="${PREFIX}/RadioactiveDecay${VER}" type="path"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)

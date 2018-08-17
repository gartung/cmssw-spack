from spack import *
import platform
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Geant4Toolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False)
    depends_on('geant4')

    def install(self, spec, prefix):
        values = {}
        values['GEANT4_VER'] = self.spec['geant4'].version
        values['GEANT4_PREFIX'] = self.spec['geant4'].prefix

        fname = 'geant4.xml'
        contents = str("""
<tool name="geant4" version="${GEANT4_VER}">
  <info url="http://geant4.web.cern.ch/geant4/"/>
  <use name="geant4core"/>
  <use name="geant4vis"/>
  <use name="xerces-c"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)

        fname = 'geant4core.xml'
        contents = str("""
<tool name="geant4core" version="${GEANT4_VER}">
  <info url="http://geant4.web.cern.ch/geant4/"/>
  <lib name="G4digits_hits"/>
  <lib name="G4error_propagation"/>
  <lib name="G4event"/>
  <lib name="G4geometry"/>
  <lib name="G4global"/>
  <lib name="G4graphics_reps"/>
  <lib name="G4intercoms"/>
  <lib name="G4interfaces"/>
  <lib name="G4materials"/>
  <lib name="G4parmodels"/>
  <lib name="G4particles"/>
  <lib name="G4persistency"/>
  <lib name="G4physicslists"/>
  <lib name="G4processes"/>
  <lib name="G4readout"/>
  <lib name="G4run"/>
  <lib name="G4tracking"/>
  <lib name="G4track"/>
  <lib name="G4analysis"/>
  <flags CXXFLAGS="-DG4MULTITHREADED -DG4USE_STD11 -ftls-model=global-dynamic -pthread"/>
  <client>
    <environment name="GEANT4_BASE" default="${GEANT4_PREFIX}"/>
    <environment name="LIBDIR" default="$$GEANT4_BASE/lib"/>
    <environment name="G4LIB" value="$$LIBDIR"/>
    <environment name="INCLUDE" default="$$GEANT4_BASE/include/Geant4"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH"  value="$$INCLUDE" type="path"/>
  <flags cppdefines="GNU_GCC G4V9"/>
  <use name="clhep"/>
  <use name="root_cxxdefaults"/>
  <flags SKIP_TOOL_SYMLINKS="1"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)

        fname = 'geant4data.xml'
        contents = str("""
<tool name="geant4data" version="${GEANT4_VER}">
  <use name="geant4data_g4abla"/>
  <use name="geant4data_g4emlow"/>
  <use name="geant4data_g4ensdfstate"/>
  <use name="geant4data_g4ndl"/>
  <use name="geant4data_g4neutronsxs"/>
  <use name="geant4data_g4photonevaporation"/>
  <use name="geant4data_g4radioactivedecay"/>
  <use name="geant4data_g4saiddata"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)

        fname = 'geant4vis.xml'
        contents = str("""
<tool name="geant4vis" version="${GEANT4_VER}">
  <info url="http://geant4.web.cern.ch/geant4/"/>
  <lib name="G4FR"/>
  <lib name="G4modeling"/>
  <lib name="G4RayTracer"/>
  <lib name="G4Tree"/>
  <lib name="G4visHepRep"/>
  <lib name="G4vis_management"/>
  <lib name="G4visXXX"/>
  <lib name="G4VRML"/>
  <lib name="G4GMocren"/>
  <lib name="G4zlib"/>
  <use name="geant4core"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)

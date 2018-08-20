from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class TauolappToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('tauolapp')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'tauolapp.xml'
        contents = str("""
<tool name="tauolapp" version="${VER}">
  <lib name="TauolaCxxInterface"/>
  <lib name="TauolaFortran"/>
  <lib name="TauolaTauSpinner"/>
  <client>
    <environment name="TAUOLAPP_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$TAUOLAPP_BASE/lib"/>
    <environment name="INCLUDE" default="$$TAUOLAPP_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="hepmc"/>
  <use name="f77compiler"/>
  <use name="pythia8"/>
  <use name="lhapdf"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname, prefix)

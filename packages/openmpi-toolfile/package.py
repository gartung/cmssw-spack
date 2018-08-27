from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class OpenmpiToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('openmpi@2.1.4')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['openmpi'].version
        values['PFX'] = self.spec['openmpi'].prefix
        fname = 'openmpi.xml'
        contents = str("""
<tool name="openmpi" version="$VER">
  <lib name="mpi"/>
  <lib name="mpi_cxx"/>
  <client>
    <environment name="OPENMPI_BASE" default="$PFX"/>
    <environment name="INCLUDE" default="$$OPENMPI_BASE/include"/>
    <environment name="LIBDIR" default="$$OPENMPI_BASE/lib"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

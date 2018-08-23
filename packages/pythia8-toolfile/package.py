from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Pythia8Toolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('pythia8')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['pythia8'].version
        values['PFX'] = spec['pythia8'].prefix

        fname = 'pythia8.xml'
        contents = str("""
<tool name="pythia8" version="${VER}">
  <lib name="pythia8"/>
  <client>
    <environment name="PYTHIA8_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$PYTHIA8_BASE/lib"/>
    <environment name="INCLUDE" default="$$PYTHIA8_BASE/include"/>
  </client>
  <runtime name="PYTHIA8DATA" value="$$PYTHIA8_BASE/share/Pythia8/xmldoc"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="cxxcompiler"/>
  <use name="hepmc"/>
  <use name="lhapdf"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname, prefix)

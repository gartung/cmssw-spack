from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class EvtgenToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('evtgen')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['evtgen'].version
        values['PFX'] = spec['evtgen'].prefix
        fname = 'evtgen.xml'
        contents = str("""
<tool name="evtgen" version="${VER}">
  <lib name="EvtGen"/>
  <lib name="EvtGenExternal"/>
  <client>
    <environment name="EVTGEN_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$EVTGEN_BASE/lib"/>
    <environment name="INCLUDE" default="$$EVTGEN_BASE/include"/>
  </client>
  <runtime name="EVTGENDATA" value="$$EVTGEN_BASE/share"/>
  <use name="hepmc"/>
  <use name="pythia8"/>
  <use name="tauolapp"/>
  <use name="photospp"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

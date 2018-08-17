from spack import *
import glob
import shutil
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class EvtgenToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False)
    depends_on('evtgen')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['evtgen'].version
        values['PFX'] = self.spec['evtgen'].prefix
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
        write_scram_toolfile(contents, values, fname)

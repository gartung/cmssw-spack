from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class SherpaToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('sherpa')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['sherpa'].version
        values['PFX'] = spec['sherpa'].prefix

        fname = 'sherpa.xml'
        contents = str("""
<tool name="sherpa" version="${VER}">
  <lib name="SherpaMain"/>
  <lib name="ToolsMath"/>
  <lib name="ToolsOrg"/>
  <client>
    <environment name="SHERPA_BASE" default="${PFX}"/>
    <environment name="BINDIR" default="$$SHERPA_BASE/bin"/>
    <environment name="LIBDIR" default="$$SHERPA_BASE/lib/SHERPA-MC"/>
    <environment name="INCLUDE" default="$$SHERPA_BASE/include/SHERPA-MC"/>
  </client>
  <runtime name="CMSSW_FWLITE_INCLUDE_PATH" value="$$SHERPA_BASE/include" type="path"/>
  <runtime name="SHERPA_SHARE_PATH" value="$$SHERPA_BASE/share/SHERPA-MC" type="path"/>
  <runtime name="SHERPA_INCLUDE_PATH" value="$$SHERPA_BASE/include/SHERPA-MC" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <runtime name="PYTHONPATH" value="$$SHERPA_BASE/lib/python2.7/site-packages" type="path"/>
  <runtime name="SHERPA_LIBRARY_PATH" value="$$SHERPA_BASE/lib/SHERPA-MC" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="HepMC"/>
  <use name="lhapdf"/>
  <use name="qd"/>
  <use name="blackhat"/>
  <use name="fastjet"/>
  <use name="sqlite"/>
  <use name="openmpi"/>
  <use name="openloops"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)


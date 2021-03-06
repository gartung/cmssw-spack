from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class CsctrackfinderemulationToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('csctrackfinderemulation')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['csctrackfinderemulation'].version
        values['PFX'] = spec['csctrackfinderemulation'].prefix
        fname = 'csctrackfinderemulation.xml'
        contents = str("""
<tool name="CSCTrackFinderEmulation" version="${VER}">
  <lib name="CSCTrackFinderEmulation"/>
  <client>
    <environment name="CSCTRACKFINDEREMULATION_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$CSCTRACKFINDEREMULATION_BASE/lib64"/>
    <environment name="INCLUDE" default="$$CSCTRACKFINDEREMULATION_BASE/include"/>
  </client>
  <runtime name="CSC_TRACK_FINDER_DATA_DIR" default="$$CSCTRACKFINDEREMULATION_BASE/data/"/>
  <runtime name="CMSSW_SEARCH_PATH" default="$$CSCTRACKFINDEREMULATION_BASE/data" type="path"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

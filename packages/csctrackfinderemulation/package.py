from spack import *
import distutils.dir_util as du
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Csctrackfinderemulation(Package):


    homepage = "http://www.example.com"
    url      = "http://www.example.com/example-1.2.3.tar.gz"

    version('1.2', git='https://github.com/cms-externals/CSCTrackFinderEmulation', branch='cms/CMSSW_8_1_X')


    def install(self, spec, prefix):
        make()
        make('install')
        du.copy_tree('installDir',prefix)

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

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
        write_scram_toolfile(contents, values, fname)

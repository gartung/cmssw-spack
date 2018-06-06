from spack import *
from glob import glob
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class FireworksGeometry(Package):



    homepage = "http://www.example.com"
    url = "https://github.com/cms-data/Fireworks-Geometry/archive/V07-05-01.tar.gz"

    version('07.05.01', '9f40fdf89286392d1d39d5ed52981051')
    version('07.05.02', '0277dd37c0ff7664ea733445445efb6a')
    version('07.05.03', 'cea2d9a9c03cb95470552f7fd73d3537')


    def install(self, spec, prefix):
        matches = []
        instpath = prefix.share+'/data/'
        mkdirp(instpath)
        for m in glob('*.root'):
            install(m, join_path(instpath, m))

    def url_for_version(self, version):
        """Handle CMSSW's version string."""
        return "https://github.com/cms-data/Fireworks-Geometry/archive/V%s.tar.gz" % version.dashed







    @run_after('install')
    def write_scram_toolfiles(self):





        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix.share + '/data'

        fname = 'fireworks-geometry.xml'
        contents = str("""
<tool name="fwlitedata" version="${VER}">
  <client>
    <environment name="CMSSWDATA_BASE" default="${PFX}"/>
    <environment name="CMSSW_DATA_PATH" default="$$CMSSWDATA_BASE"/>
  </client>
  <runtime name="CMSSW_DATA_PATH" value="$$CMSSWDATA_BASE" handler="warn" type="path"/>
  <runtime name="CMSSW_SEARCH_PATH" default="${PFX}" handler="warn" type="path"/>
</tool>
""")


        write_scram_toolfile(contents, values, fname)

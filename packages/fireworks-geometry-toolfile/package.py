from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class FireworksGeometryToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('fireworks-geometry')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['fireworks-geometry'].version
        values['PFX'] = spec['fireworks-geometry'].prefix.share + '/data'
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
        write_scram_toolfile(contents, values, fname, prefix)

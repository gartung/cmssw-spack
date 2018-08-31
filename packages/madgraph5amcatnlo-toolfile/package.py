from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Madgraph5amcatnloToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('madgraph5amcatnlo')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['madgraph5amcatnlo'].version
        values['PFX'] = spec['madgraph5amcatnlo'].prefix

        fname = 'madgraph5amcatnlo.xml'
        contents = str("""
<tool name="madgraph5amcatnlo" version="$VER">
  <client>
    <environment name="MADGRAPH5AMCATNLO_BASE" default="$PFX"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$MADGRAPH5AMCATNLO_BASE" type="path"/>
  <runtime name="ROOT_PATH" value="$$MADGRAPH5AMCATNLO_BASE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="gosamcontrib"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname, prefix)

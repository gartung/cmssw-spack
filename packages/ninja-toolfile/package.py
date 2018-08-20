from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class NinjaToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('ninja')

    def install(self, spec, prefix):
        values={}
        values['PFX']=prefix
        values['VER']=self.version
        fname='ninja.xml'
        contents="""
<tool name="ninja" version="${VER}">
  <client>
    <environment name="NINJA_BASE" default="${PFX}"/>
  </client>
  <runtime name="PATH" value="$$NINJA_BASE/bin" type="path"/>
</tool>
"""
        write_scram_toolfile(fname, contents, values, prefix)

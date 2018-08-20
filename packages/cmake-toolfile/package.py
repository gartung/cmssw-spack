from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class CmakeToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('cmake')

    def install(self, spec, prefix):
        values={}
        values['PFX']=spec['cmake'].prefix
        values['VER']=spec['cmake'].version
        fname='cmake.xml'
        contents=str("""
<tool name="ninja" version="${VER}">
  <client>
    <environment name="CMAKE_BASE" default="${PFX}"/>
  </client>
  <runtime name="PATH" value="$$CMAKE_BASE/bin" type="path"/>
</tool>
""")
        write_scram_toolfile(fname, contents, values, prefix)

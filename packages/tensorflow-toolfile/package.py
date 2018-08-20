from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class TensorflowToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('tensorflow')

    def install(self, spec, prefix):
        values = {}
        values['PFX']=spec['tensorflow'].prefix
        values['VER']=spec['tensorflow'].version
        fname='tensorflow.xml'
        content=str("""
<tool name="tensorflow" version="${VER}">
  <client>
    <environment name="TENSORFLOW_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$TENSORFLOW_BASE/lib"/>
    <environment name="INCLUDE" default="$$TENSORFLOW_BASE/include"/>
    <environment name="TFCOMPILE" default="$$TENSORFLOW_BASE/bin/tfcompile"/>
  </client>
  <runtime name="PATH" value="$$TENSORFLOW_BASE/bin" type="path"/>
</tool>
""")
        write_scram_toolfile(content, values, fname, prefix)

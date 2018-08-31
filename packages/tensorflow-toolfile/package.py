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

        fname='tensorflow-framework.xml'
        content=str("""
<tool name="tensorflow-framework" version="${VER}">
  <lib name="tensorflow_framework"/>
  <use name="tensorflow"/>
</tool>
""")
        write_scram_toolfile(content, values, fname, prefix)

        fname='tensorflow-cc.xml'
        content=str("""
<tool name="tensorflow-cc" version="${VER}">
  <lib name="tensorflow_cc"/>
  <use name="tensorflow-framework"/>
  <use name="eigen"/>
  <use name="protobuf"/>
</tool>
""")
        write_scram_toolfile(content, values, fname, prefix)

        name='tensorflow-c.xml'
        content=str("""
<tool name="tensorflow-c" version="${VER}">
  <lib name="tensorflow"/>
  <use name="tensorflow-framework"/>
</tool>
""")
        write_scram_toolfile(content, values, fname, prefix)

        name='tensorflow-runtime.xml'
        content=str("""
<tool name="tensorflow-runtime" version="${VER}">
  <lib name="tf_aot_runtime"/>
  <use name="tensorflow"/>
</tool>
""")
        write_scram_toolfile(content, values, fname, prefix)

        name='tensorflow-xla_compiled_cpu_function.xml'
        content=str("""
<tool name="tensorflow-xla_compiled_cpu_function" version="@TOOL_VERSION@">
  <lib name="xla_compiled_cpu_function"/>
  <use name="tensorflow"/>
</tool>
""")
        write_scram_toolfile(content, values, fname, prefix)

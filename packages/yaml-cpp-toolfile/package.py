from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class YamlCppToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('yaml-cpp')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['yaml-cpp'].version
        values['PFX'] = spec['yaml-cpp'].prefix

        fname = 'yamlcpp.xml'
        contents = str("""
<tool name="yaml-cpp" version="${VER}">
  <info url="http://code.google.com/p/yaml-cpp/"/>
  <lib name="yaml-cpp"/>
  <client>
    <environment name="YAML_CPP_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$YAML_CPP_BASE/lib"/>
    <environment name="INCLUDE" default="$$YAML_CPP_BASE/include"/>
  </client>
  <use name="boost"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

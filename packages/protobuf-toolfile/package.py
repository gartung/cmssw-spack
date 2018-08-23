from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class ProtobufToolfile(Package):

    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('protobuf')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['protobuf'].version
        values['PFX'] = spec['protobuf'].prefix

        fname = 'protobuf.xml'
        contents = str("""
<tool name="protobuf" version="${VER}">
  <lib name="protobuf"/>
  <client>
    <environment name="PROTOBUF_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$PROTOBUF_BASE/include"/>
    <environment name="LIBDIR" default="$$PROTOBUF_BASE/lib"/>
    <environment name="BINDIR" default="$$PROTOBUF_BASE/bin"/>
  </client>
  <runtime name="PATH" value="$$PROTOBUF_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <flags SKIP_TOOL_SYMLINKS="1"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname, prefix)

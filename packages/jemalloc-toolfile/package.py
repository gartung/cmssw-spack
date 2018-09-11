from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile

class JemallocToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('jemalloc')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['jemalloc'].version
        values['PFX'] = spec['jemalloc'].prefix
        fname = 'jemalloc.xml'
        contents = str("""
<tool name="jemalloc" version="${VER}">
  <architecture name="slc.*|fc.*|linux*">
    <lib name="jemalloc"/>
  </architecture>
  <client>
    <environment name="JEMALLOC_BASE" default="${PFX}"/>
    <environment name="LIBDIR"        default="$$JEMALLOC_BASE/lib"/>
    <environment name="INCLUDE"        default="$$JEMALLOC_BASE/include"/>
  </client>
  <runtime name="MALLOC_CONF" value="lg_chunk:18,lg_dirty_mult:4"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <flags SKIP_TOOL_SYMLINKS="1"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

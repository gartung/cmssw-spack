from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class McdbToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('mcdb')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['mcdb'].version
        values['PFX'] = spec['mcdb'].prefix

        fname = 'mcdb.xml'
        contents = str("""
<tool name="mcdb" version="$VER">
  <lib name="mcdb"/>
  <client>
    <environment name="MCDB_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$MCDB_BASE/lib"/>
    <environment name="INCLUDE" default="$$MCDB_BASE/interface"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="xerces-c"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

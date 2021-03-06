from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Bzip2Toolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('bzip2')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['bzip2'].version
        values['PFX'] = spec['bzip2'].prefix

        fname = 'bz2lib.xml'
        contents = str("""<tool name="bz2lib" version="$VER">
  <lib name="bz2"/>
  <client>
    <environment name="BZ2LIB_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$BZ2LIB_BASE/lib"/>
    <environment name="INCLUDE" default="$$BZ2LIB_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

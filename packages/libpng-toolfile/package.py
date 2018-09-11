from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class LibpngToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('libpng@1.6.16')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['libpng'].version
        values['PFX'] = spec['libpng'].prefix

        fname = 'libpng.xml'
        contents = str("""<tool name="libpng" version="$VER">
  <info url="http://www.libpng.org/"/>
  <lib name="png"/>
  <client>
    <environment name="LIBPNG_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$LIBPNG_BASE/lib"/>
    <environment name="INCLUDE" default="$$LIBPNG_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="zlib"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

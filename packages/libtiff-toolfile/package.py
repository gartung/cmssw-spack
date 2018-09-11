from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class LibtiffToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('libtiff@4.0.3')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['libtiff'].version
        values['PFX'] = spec['libtiff'].prefix

        fname = 'libtiff.xml'
        contents = str("""<tool name="libtiff" version="$VER">
  <info url="http://www.libtiff.org/"/>
  <lib name="tiff"/>
  <client>
    <environment name="LIBTIFF_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$LIBTIFF_BASE/lib"/>
    <environment name="INCLUDE" default="$$LIBTIFF_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="libjpeg-turbo"/>
  <use name="zlib"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class GiflibToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('giflib')

    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = spec['giflib'].version
        values['PFX'] = spec['giflib'].prefix
        fname = 'giflib.xml'
        contents = str("""<tool name="giflib" version="$VER">
    <info url="http://giflib.sourceforge.net"/>
    <lib name="gif"/>
    <client>
      <environment name="GIFLIB_BASE" default="$PFX"/>
      <environment name="LIBDIR" default="$$GIFLIB_BASE/lib"/>
      <environment name="INCLUDE" default="$$GIFLIB_BASE/include"/>
    </client>
    <runtime name="PATH" value="$$GIFLIB_BASE/bin" type="path"/>
    <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
    <use name="root_cxxdefaults"/>
  </tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

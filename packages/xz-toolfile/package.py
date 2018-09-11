from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class XzToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('xz@5.2.2')


    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['xz'].version
        values['PFX'] = spec['xz'].prefix

        fname = 'xz.xml'
        contents = str("""<tool name="xz" version="$VER">
    <info url="http://tukaani.org/xz/"/>
    <lib name="lzma"/>
    <client>
      <environment name="XZ_BASE" default="$PFX"/>
      <environment name="LIBDIR" default="$$XZ_BASE/lib"/>
      <environment name="INCLUDE" default="$$XZ_BASE/include"/>
    </client>
    <runtime name="PATH" value="$$XZ_BASE/bin" type="path"/>
    <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
    <use name="root_cxxdefaults"/>
  </tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

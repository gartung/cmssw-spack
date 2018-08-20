from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class LhapdfToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('lhapdf')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['lhapdf'].version
        values['PFX'] = spec['lhapdf'].prefix

        fname = 'lhapdf.xml'
        contents = str("""
<tool name="lhapdf" version="${VER}">
  <lib name="LHAPDF"/>
  <client>
    <environment name="LHAPDF_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$LHAPDF_BASE/lib"/>
    <environment name="INCLUDE" default="$$LHAPDF_BASE/include"/>
  </client>
  <runtime name="LHAPDF_DATA_PATH" value="$$LHAPDF_BASE/share/LHAPDF"/>
  <use name="yaml-cpp"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

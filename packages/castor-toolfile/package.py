from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class CastorToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('castor')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['castor'].version
        values['PFX'] = spec['castor'].prefix

        fname = 'castor_header.xml'
        contents = str("""
<tool name="castor_header" version="${VER}">
  <client>
    <environment name="CASTOR_HEADER_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$CASTOR_HEADER_BASE/include"/>
    <environment name="INCLUDE" default="$$CASTOR_HEADER_BASE/include/shift"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$CASTOR_HEADER_BASE/include" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$CASTOR_HEADER_BASE/include/shift" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

        fname = 'castor.xml'
        contents = str("""
<tool name="castor" version="${VER}">
  <lib name="shift"/>
  <lib name="castorrfio"/>
  <lib name="castorclient"/>
  <lib name="castorcommon"/>
  <client>
    <environment name="CASTOR_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$CASTOR_BASE/lib"/>
  </client>
  <runtime name="PATH" value="$$CASTOR_BASE/bin" type="path"/>
  <use name="castor_header"/>
  <use name="libuuid"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

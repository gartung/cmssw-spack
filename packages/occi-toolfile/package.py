from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class OcciToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('occi-cms')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['occi-cms'].version
        values['PFX'] = spec['occi-cms'].prefix

        fname = 'cms-occi.xml'
        contents = str("""
<tool name="oracleocci" version="${VER}">
  <lib name="cms_oracleocci_abi_hack"/>
  <use name="oracleocci-official"/>
  <client>
    <environment name="ORACLEOCCI_BASE" default="${PFX}"/>
    <environment name="INCLUDE" value="${PFX}/include"/>
    <environment name="LIBDIR" value="${PFX}/lib"/>
  </client>
  <runtime name="CMS_ORACLEOCCI_LIB" value="$$LIBDIR/libcms_oracleocci_abi_hack.so"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

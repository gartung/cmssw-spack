from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class VecgeomToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)

    depends_on('vecgeom@v00.05.00')

    def install(self, spec, prefix):
        values = {}
        values['PFX']=spec['vecgeom'].prefix
        values['VER']=spec['vecgeom'].version
        fname='vecgeom_interface.xml'
        contents=str("""
<tool name="vecgeom_interface" version="${VER}">
  <info url="https://gitlab.cern.ch/VecGeom/VecGeom"/>
  <client>
    <environment name="VECGEOM_INTERFACE_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$VECGEOM_INTERFACE_BASE/include"/>
  </client>
  <flags CPPDEFINES="VECGEOM_SCALAR"/>
  <flags CPPDEFINES="VECGEOM_REPLACE_USOLIDS"/>
  <flags CPPDEFINES="VECGEOM_NO_SPECIALIZATION"/>
  <flags CPPDEFINES="VECGEOM_USOLIDS"/>
  <flags CPPDEFINES="VECGEOM_INPLACE_TRANSFORMATIONS"/>
  <flags CPPDEFINES="VECGEOM_USE_INDEXEDNAVSTATES"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

        fname="vecgeom.xml"
        contents=str("""
<tool name="vecgeom" version="${VER}">
  <info url="https://gitlab.cern.ch/VecGeom/VecGeom"/>
  <lib name="vecgeom"/>
  <lib name="usolids"/>
  <client>
    <environment name="VECGEOM_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$VECGEOM_BASE/lib"/>
  </client>
  <use name="vecgeom_interface"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)


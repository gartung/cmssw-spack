from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class TkonlineswToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('tkonlinesw')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'tkonlinesw.xml'
        contents = str("""
<tool name="TkOnlineSw" version="${VER}">
  <info url="http://www.cern.ch/"/>
  <lib name="ICUtils"/>
  <lib name="Fed9UUtils"/>
  <client>
    <environment name="TKONLINESW_BASE" default="${PFX}"/>
    <environment name="LIBDIR" value="$$TKONLINESW_BASE/lib"/>
    <environment name="INCLUDE" value="$$TKONLINESW_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <flags CXXFLAGS="-DCMS_TK_64BITS"/>
  <use name="root_cxxdefaults"/>
  <use name="xerces-c"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname, prefix)

        fname = 'tkonlineswdb.xml'
        contents = str("""
<tool name="TkOnlineSwDB" version="${VER}">
  <info url="http://www.cern.ch/"/>
  <lib name="DeviceDescriptions"/>
  <lib name="Fed9UDeviceFactory"/>
  <use name="tkonlinesw"/>
  <use name="oracle"/>
  <use name="oracleocci"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname, prefix)

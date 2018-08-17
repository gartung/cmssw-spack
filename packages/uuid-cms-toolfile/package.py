from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class UuidCmsToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False)
    depends_on('uuid-cms')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['uuid-cms'].version
        values['PFX'] = self.spec['uuid-cms'].prefix
        fname = 'uuid-cms.xml'
        contents = str("""<tool name="uuid" version="$VER">
  <lib name="uuid"/>
  <client>
    <environment name="LIBUUID_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$LIBUUID_BASE/lib"/>
    <environment name="INCLUDE" default="$$LIBUUID_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="sockets"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)

        fname = 'libuuid.xml'
        contents = str("""<tool name="libuuid" version="$VER">
  <lib name="uuid"/>
  <client>
    <environment name="LIBUUID_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$LIBUUID_BASE/lib"/>
    <environment name="INCLUDE" default="$$LIBUUID_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="sockets"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)

from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class FrontierClientToolfile(MakefilePackage):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False)
    depends_on('frontier-client')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['frontier-client'].version
        values['PFX'] = self.spec['frontier-client'].prefix
        fname = 'frontier_client.xml'
        contents = str("""<tool name="frontier_client" version="$VER">
  <lib name="frontier_client"/>
  <client>
    <environment name="FRONTIER_CLIENT_BASE" default="$PFX"/>
    <environment name="INCLUDE" default="$$FRONTIER_CLIENT_BASE/include"/>
    <environment name="LIBDIR" default="$$FRONTIER_CLIENT_BASE/lib"/>
  </client>
  <runtime name="FRONTIER_CLIENT" value="$$FRONTIER_CLIENT_BASE/"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="zlib"/>
  <use name="openssl"/>
  <use name="expat"/>
  <runtime name="PYTHONPATH" value="$$FRONTIER_CLIENT_BASE/python/lib" type="path"/>
  <use name="python"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)

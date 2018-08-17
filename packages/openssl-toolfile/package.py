from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class OpensslToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False)
    depends_on('openssl')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['openssl'].version
        values['PFX'] = self.spec['openssl'].prefix
        fname = 'openssl.xml'
        contents = str("""<tool name="openssl" version="$VER">
    <lib name="ssl"/>
    <lib name="crypto"/>
    <client>
      <environment name="OPENSSL_BASE" default="$PFX"/>
      <environment name="INCLUDE" default="$$OPENSSL_BASE/include"/>
      <environment name="LIBDIR" default="$$OPENSSL_BASE/lib"/>
    </client>
    <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
    <use name="root_cxxdefaults"/>
  </tool>""")
        write_scram_toolfile(contents, values, fname)

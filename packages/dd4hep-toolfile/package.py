from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Dd4hepToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False)
    depends_on('dd4hep')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['dd4hep'].version
        values['PFX'] = self.spec['dd4hep'].prefix
        fname = 'openssl.xml'
        contents = str("""
<tool name="dd4hep" version="$VER">
  <info url="https://github.com/AIDASoft/DD4hep"/>
  <lib name="DDAlign" />
  <lib name="DDCore" />
  <lib name="DDCond" />
  <lib name="DDParsers" />
  <client>
    <environment name="DD4HEP_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$DD4HEP_BASE/lib"/>
    <environment name="INCLUDE" default="$$DD4HEP_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <runtime name="PATH" value="$$DD4HEP_BASE/bin" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="root"/>
  <use name="boost"/>
  <use name="xerces-c"/>
  <use name="clhep"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)


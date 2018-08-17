from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class CppunitToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False)
    depends_on('cppunit')

    def install(self,spec,prefix):
        values = {}
        values['VER'] = self.spec['cppunit'].version
        values['PFX'] = self.spec['cppunit'].prefix
        fname = 'cppunit.xml'
        contents = str("""<tool name="cppunit" version="$VER">
  <lib name="cppunit"/>
  <client>
    <environment name="CPPUNIT_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$CPPUNIT_BASE/lib"/>
    <environment name="INCLUDE" default="$$CPPUNIT_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="sockets"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)

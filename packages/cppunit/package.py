from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Cppunit(AutotoolsPackage):
    """Obsolete Unit testing framework for C++"""

    homepage = "https://wiki.freedesktop.org/www/Software/cppunit/"
    url = "http://dev-www.libreoffice.org/src/cppunit-1.13.2.tar.gz"

    version('1.13.2', '0eaf8bb1dcf4d16b12bec30d0732370390d35e6f')

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

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

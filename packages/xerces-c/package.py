from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class XercesC(AutotoolsPackage):
    """Xerces-C++ is a validating XML parser written in a portable subset of
    C++. Xerces-C++ makes it easy to give your application the ability to read
    and write XML data. A shared library is provided for parsing, generating,
    manipulating, and validating XML documents using the DOM, SAX, and SAX2
    APIs."""

    homepage = "https://xerces.apache.org/xerces-c"
    url = "https://archive.apache.org/dist/xerces/c/3/sources/xerces-c-3.1.4.tar.bz2"

    version('3.1.4', 'd04ae9d8b2dee2157c6db95fa908abfd')

    def configure_args(self):
        return ['--disable-network']


    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'xerces-c.xml'
        contents = str("""<tool name="xerces-c" version="$VER">
  <info url="http://xml.apache.org/xerces-c/"/>
  <lib name="xerces-c"/>
  <client>
    <environment name="XERCES_C_BASE" default="$PFX"/>
    <environment name="INCLUDE" default="$$XERCES_C_BASE/include"/>
    <environment name="LIBDIR" default="$$XERCES_C_BASE/lib"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")

        write_scram_toolfile(contents, values, fname)

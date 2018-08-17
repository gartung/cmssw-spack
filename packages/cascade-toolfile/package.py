from spack import *
import glob
import distutils.dir_util as du
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile 


class CascadeToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False)
    depends_on('cascade')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['cascade'].version
        values['PFX'] = self.spec['cascase'].prefix

        fname = 'cascade.xml'
        contents = str("""
<tool name="cascade" version="${VER}">
    <lib name="cascade_merged"/>
  <client>
    <environment name="CASCADE_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$CASCADE_BASE/lib"/>
  </client>
  <runtime name="CASCADE_PDFPATH" value="$$CASCADE_BASE/share"/>
  <use name="f77compiler"/>
  <use name="cascade_headers"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)

        fname = 'cascade_headers.xml'
        contents = str("""
<tool name="cascade_headers" version="${VER}">
  <client>
    <environment name="CASCADE_HEADERS_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$CASCADE_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)


from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Vdt(CMakePackage):
    """Vectorised math. A collection of fast and inline implementations of
    mathematical functions."""

    homepage = "https://github.com/dpiparo/vdt"
    url = "https://github.com/dpiparo/vdt/archive/v0.3.9.tar.gz"

    version('0.3.9', '80a2d73a82f7ef8257a8206ca22dd145')
    version('0.3.8', '25b07c72510aaa95fffc11e33579061c')
    version('0.3.7', 'd2621d4c489894fd1fe8e056d9a0a67c')
    version('0.3.6', '6eaff3bbbd5175332ccbd66cd71a741d')


    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'vdt_headers.xml'
        contents = str("""<tool name="vdt_headers" version="$VER">
  <client>
    <environment name="VDT_HEADERS_BASE" default="$PFX"/>
    <environment name="INCLUDE" default="$$VDT_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")

        write_scram_toolfile(contents, values, fname)

        fname = 'vdt.xml'
        contents = str("""<tool name="vdt" version="$VER">
  <lib name="vdt"/>
  <use name="vdt_headers"/>
  <client>
    <environment name="VDT_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$VDT_BASE/lib"/>
  </client>
</tool>""")

        write_scram_toolfile(contents, values, fname)

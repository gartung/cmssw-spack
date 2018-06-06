from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile



class Giflib(AutotoolsPackage):
    """The GIFLIB project maintains the giflib service library, which has
    been pulling images out of GIFs since 1989."""

    homepage = "http://giflib.sourceforge.net/"
    url = "https://downloads.sourceforge.net/project/giflib/giflib-5.1.4.tar.bz2"

    version('5.1.4', '2c171ced93c0e83bb09e6ccad8e3ba2b')

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'giflib.xml'
        contents = str("""<tool name="giflib" version="$VER">
    <info url="http://giflib.sourceforge.net"/>
    <lib name="gif"/>
    <client>
      <environment name="GIFLIB_BASE" default="$PFX"/>
      <environment name="LIBDIR" default="$$GIFLIB_BASE/lib"/>
      <environment name="INCLUDE" default="$$GIFLIB_BASE/include"/>
    </client>
    <runtime name="PATH" value="$$GIFLIB_BASE/bin" type="path"/>
    <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
    <use name="root_cxxdefaults"/>
  </tool>""")

        write_scram_toolfile(contents, values, fname)

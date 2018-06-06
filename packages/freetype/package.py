from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Freetype(AutotoolsPackage):
    """FreeType is a freely available software library to render fonts.
    It is written in C, designed to be small, efficient, highly customizable,
    and portable while capable of producing high-quality output (glyph images)
    of most vector and bitmap font formats."""

    homepage = "https://www.freetype.org/index.html"
    url = "http://download.savannah.gnu.org/releases/freetype/freetype-2.7.1.tar.gz"

    version('2.7.1', '78701bee8d249578d83bb9a2f3aa3616')
    version('2.7',   '337139e5c7c5bd645fe130608e0fa8b5')
    version('2.5.3', 'cafe9f210e45360279c730d27bf071e9')

    depends_on('libpng')
    depends_on('bzip2')
    depends_on('pkg-config@0.24:', type='build')

    def configure_args(self):
        return ['--with-harfbuzz=no']







    @run_after('install')
    def write_scram_toolfiles(self):





        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'freetype.xml'
        contents = str("""
<tool name="freetype" version="${VER}">
  <lib name="freetype-cms"/>
  <client>
    <environment name="FREETYPE_BASE" default="${PFX}"/>
    <environment name="INCLUDE"      default="$$FREETYPE_BASE/include"/>
    <environment name="LIBDIR"       default="$$FREETYPE_BASE/lib"/>
  </client>
  <runtime name="PATH" value="$$FREETYPE_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")


        write_scram_toolfile(contents, values, fname)

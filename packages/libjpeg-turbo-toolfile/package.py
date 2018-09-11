from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile

class LibjpegTurboToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('libjpeg-turbo@1.3.1')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec["libjpeg-turbo"].version
        values['PFX'] = spec["libjpeg-turbo"].prefix

        fname = 'libjpg.xml'
        contents = str("""<tool name="libjpeg-turbo" version="$VER">
  <info url="http://libjpeg-turbo.virtualgl.org"/>
  <lib name="jpeg"/>
  <lib name="turbojpeg"/>
  <client>
    <environment name="LIBJPEG_TURBO_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$LIBJPEG_TURBO_BASE/lib64"/>
    <environment name="INCLUDE" default="$$LIBJPEG_TURBO_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <runtime name="PATH" value="$$LIBJPEG_TURBO_BASE/bin" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

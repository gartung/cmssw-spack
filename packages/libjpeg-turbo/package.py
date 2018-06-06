from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class LibjpegTurbo(AutotoolsPackage):
    """libjpeg-turbo is a fork of the original IJG libjpeg which uses SIMD to
       accelerate baseline JPEG compression and decompression. libjpeg is a
       library that implements JPEG image encoding, decoding and
       transcoding."""

    homepage = "http://libjpeg-turbo.virtualgl.org"
    url = "http://downloads.sourceforge.net/libjpeg-turbo/libjpeg-turbo-1.3.1.tar.gz"

    version('1.5.0', '3fc5d9b6a8bce96161659ae7a9939257')
    version('1.3.1', '2c3a68129dac443a72815ff5bb374b05')

    provides('jpeg')

    # Can use either of these. But in the current version of the package
    # only nasm is used. In order to use yasm an environmental variable
    # NASM must be set.
    # TODO: Implement the selection between two supported assemblers.
    # depends_on("yasm", type='build')
    depends_on("nasm", type='build')


    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'libjpg.xml'
        contents = str("""<tool name="libjpeg-turbo" version="$VER">
  <info url="http://libjpeg-turbo.virtualgl.org"/>
  <lib name="jpeg"/>
  <lib name="turbojpeg"/>
  <client>
    <environment name="LIBJPEG_TURBO_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$LIBJPEG_TURBO_BASE/lib"/>
    <environment name="INCLUDE" default="$$LIBJPEG_TURBO_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <runtime name="PATH" value="$$LIBJPEG_TURBO_BASE/bin" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")

        write_scram_toolfile(contents, values, fname)

from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Xz(AutotoolsPackage):
    """XZ Utils is free general-purpose data compression software with
       high compression ratio. XZ Utils were written for POSIX-like
       systems, but also work on some not-so-POSIX systems. XZ Utils are
       the successor to LZMA Utils."""
    homepage = "http://tukaani.org/xz/"
    url = "http://tukaani.org/xz/xz-5.2.0.tar.bz2"
    list_url = "http://tukaani.org/xz/old.html"

    version('5.2.3', '1592e7ca3eece099b03b35f4d9179e7c')
    version('5.2.2', 'f90c9a0c8b259aee2234c4e0d7fd70af')
    version('5.2.0', '867cc8611760240ebf3440bd6e170bb9')


    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'xz.xml'
        contents = str("""<tool name="xz" version="$VER">
    <info url="http://tukaani.org/xz/"/>
    <lib name="lzma"/>
    <client>
      <environment name="XZ_BASE" default="$PFX"/>
      <environment name="LIBDIR" default="$$XZ_BASE/lib"/>
      <environment name="INCLUDE" default="$$XZ_BASE/include"/>
    </client>
    <runtime name="PATH" value="$$XZ_BASE/bin" type="path"/>
    <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
    <use name="root_cxxdefaults"/>
  </tool>""")


        write_scram_toolfile(contents, values, fname)

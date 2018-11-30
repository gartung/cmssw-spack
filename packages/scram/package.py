from spack import *
from glob import glob
from string import Template
import re
import fnmatch
import shutil
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Scram(Package):
    """SCRAM as used by CMS"""

    homepage = "https://github.com/cms-sw/SCRAM"
    url = "https://github.com/cms-sw/SCRAM/archive/V2_2_6.tar.gz"

    version('2_2_8_pre7', '8675ba547d471632d288b2e1c327a35c')
    version('2_2_8_pre6', '94b626646228f19ad7104b7de2cd22bb')
    version('2_2_8_pre1', 'b5992a1d94ba5f87517e9a5b5941a7fb')

    depends_on('gmake')

    scram_arch = 'slc_amd64_gcc'
    if sys.platform == 'darwin':
        scram_arch = 'osx10_amd64_clang'

    def install(self, spec, prefix):
        gmake = which('gmake')
        args = ['install']
        args.append('INSTALL_BASE=%s' % prefix)
        args.append('VERSION=V%s' % self.version)
        args.append('PREFIX=%s' % prefix)
        args.append('VERBOSE=1')
        gmake(*args)

        with working_dir(prefix.etc + '/scram.d', create=True):
            gcc = which(spack_f77)
            gcc_prefix = re.sub('/bin/.*$', '', self.compiler.f77)
            gcc_machine = gcc('-dumpmachine', output=str)
            gcc_ver = gcc('-dumpversion', output=str)

            values = {}
            values['GCC_VER'] = gcc_ver.rstrip()
            values['GCC_PREFIX'] = gcc_prefix
            values['GCC_MACHINE'] = gcc_machine.rstrip()
            values['PFX'] = ""
            values['VER'] = ""


            contents = str("""
  <tool name="sockets" version="1.0">
    <lib name="nsl"/>
    <lib name="crypt"/>
    <lib name="dl"/>
    <lib name="rt"/>
  </tool>
""")
            if sys.platform == 'darwin':
                contents = str("""
  <tool name="sockets" version="1.0">
    <lib name="dl"/>
  </tool>
""")
            write_scram_toolfile(contents, values, 'sockets.xml', prefix)


            contents = str("""
  <tool name="opengl" version="XFree4.2">
    <lib name="GL"/>
    <lib name="GLU"/>
    <use name="x11"/>
    <environment name="ORACLE_ADMINDIR" default="/etc"/>
""")
            if sys.platform == 'darwin':
                contents += """
    <client>
      <environment name="OPENGL_BASE" default="/System/Library/Frameworks/OpenGL.framework/Versions/A"/>
      <environment name="INCLUDE"     default="$$OPENGL_BASE/Headers"/>
      <environment name="LIBDIR"      default="$$OPENGL_BASE/Libraries"/>
    </client>
"""
            contents += """</tool>"""
            write_scram_toolfile(contents, values, 'opengl.xml', prefix)


            contents = str("""
  <tool name="x11" version="R6">
    <use name="sockets"/>
  </tool>
""")
            write_scram_toolfile(contents, values, 'x11.xml', prefix)

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('SCRAM_ARCH', self.scram_arch)

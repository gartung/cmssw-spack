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

    version('2_2_8_pre1', 'b5992a1d94ba5f87517e9a5b5941a7fb')

    depends_on('gmake')

    scram_arch = 'slc7_amd64_gcc700'
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
  <tool name="gcc-ccompiler" version="${GCC_VER}" type="compiler">
    <client>
      <environment name="GCC_CCOMPILER_BASE" default="${GCC_PREFIX}"/>
    </client>
    <flags CSHAREDOBJECTFLAGS="-fPIC   "/>
    <flags CFLAGS="-O2 -pthread   "/>
  </tool>
""")
    
            write_scram_toolfile(contents, values, 'gcc-ccompiler.xml', prefix)
    

            contents = str("""
  <tool name="gcc-cxxcompiler" version="${GCC_VER}" type="compiler">
    <client>
      <environment name="GCC_CXXCOMPILER_BASE" default="${GCC_PREFIX}"/>
    </client>
    <flags CPPDEFINES="GNU_GCC _GNU_SOURCE   "/>
    <flags CXXSHAREDOBJECTFLAGS="-fPIC   "/>
    <flags CXXFLAGS="-O2 -pthread -pipe -Werror=main -Werror=pointer-arith"/>
    <flags CXXFLAGS="-Werror=overlength-strings -Wno-vla -Werror=overflow   -std=c++1z -ftree-vectorize -Wstrict-overflow -Werror=array-bounds -Werror=format-contains-nul -Werror=type-limits -fvisibility-inlines-hidden -fno-math-errno --param vect-max-version-for-alias-checks=50 -Wa,--compress-debug-sections -fno-crossjumping -msse3"/>
    <flags CXXFLAGS="-felide-constructors -fmessage-length=0"/>
    <flags CXXFLAGS="-Wall -Wno-non-template-friend -Wno-long-long -Wreturn-type"/>
    <flags CXXFLAGS="-Wunused -Wparentheses -Wno-deprecated -Werror=return-type"/>
    <flags CXXFLAGS="-Werror=missing-braces -Werror=unused-value"/>
    <flags CXXFLAGS="-Werror=address -Werror=format -Werror=sign-compare"/>
    <flags CXXFLAGS="-Werror=write-strings -Werror=delete-non-virtual-dtor"/>
    <flags CXXFLAGS="-Werror=maybe-uninitialized -Werror=strict-aliasing"/>
    <flags CXXFLAGS="-Werror=narrowing -Werror=uninitialized"/>
    <flags CXXFLAGS="-Werror=unused-but-set-variable -Werror=reorder"/>
    <flags CXXFLAGS="-Werror=unused-variable -Werror=conversion-null"/>
    <flags CXXFLAGS="-Werror=return-local-addr"/>
    <flags CXXFLAGS="-Werror=switch -fdiagnostics-show-option"/>
    <flags CXXFLAGS="-Wno-unused-local-typedefs -Wno-attributes -Wno-psabi"/>
    <flags LDFLAGS="-Wl,-E -Wl,--hash-style=gnu  "/>
    <flags CXXSHAREDFLAGS="-shared -Wl,-E  "/>
    <flags LD_UNIT=" -r -z muldefs "/>
    <runtime name="LD_LIBRARY_PATH" value="$$GCC_CXXCOMPILER_BASE/lib64" type="path"/>
    <runtime name="LD_LIBRARY_PATH" value="$$GCC_CXXCOMPILER_BASE/lib" type="path"/>
    <runtime name="PATH" value="$$GCC_CXXCOMPILER_BASE/bin" type="path"/>
  </tool>
""")
            write_scram_toolfile(contents, values, 'gcc-cxxcompiler.xml', prefix)


            contents = str("""
  <tool name="gcc-f77compiler" version="${GCC_VER}" type="compiler">
    <lib name="gfortran"/>
    <lib name="m"/>
    <client>
      <environment name="GCC_F77COMPILER_BASE" default="${GCC_PREFIX}"/>
    </client>
    <flags FFLAGS="-fno-second-underscore -Wunused -Wuninitialized -O2 -cpp"/>
    <flags LDFLAGS="-L$$(GCC_F77COMPILER_BASE)/lib64"/>
    <flags LDFLAGS="-L$$(GCC_F77COMPILER_BASE)/lib"/>
    <flags FOPTIMISEDFLAGS="-O2   "/>
    <flags FSHAREDOBJECTFLAGS="-fPIC   "/>
  </tool>
""")
            write_scram_toolfile(contents, values, 'gcc-f77compiler.xml', prefix)


            contents = str("""
<tool name="root_cxxdefaults" version="6">
  <runtime name="ROOT_GCC_TOOLCHAIN" value="${GCC_PREFIX}" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="${GCC_PREFIX}/include/c++/${GCC_VER}" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="${GCC_PREFIX}/include/c++/${GCC_VER}/${GCC_MACHINE}" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="${GCC_PREFIX}/include/c++/${GCC_VER}/backward" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="/usr/local/include" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="/usr/include" type="path"/>
</tool>
""")
            write_scram_toolfile(contents, values, 'root_cxxdefaults.xml', prefix)


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
      <environment name="INCLUDE"     default="$OPENGL_BASE/Headers"/>
      <environment name="LIBDIR"      default="$OPENGL_BASE/Libraries"/>
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

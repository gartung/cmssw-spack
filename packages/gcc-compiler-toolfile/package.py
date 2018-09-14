from spack import *
from glob import glob
from string import Template
import re
import fnmatch
import shutil
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class GccCompilerToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)

    def install(self, spec, prefix):

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
            values['LIB'] = 'lib64'
            if sys.platform == 'darwin':
                 values['LIB'] = 'lib'

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
    
            if sys.platform == 'darwin':
                contents = str("""
  <tool name="gcc-cxxcompiler" version="${GCC_VER}" type="compiler">
    <client>
      <environment name="GCC_CXXCOMPILER_BASE" default="${GCC_PREFIX}"/>
    </client>
    <flags CPPDEFINES="GNU_GCC _GNU_SOURCE   "/>
    <flags CXXSHAREDOBJECTFLAGS="-fPIC   "/>
    <flags REM_CXXFLAGS="-Wno-non-template-friend"/>
    <flags REM_CXXFLAGS="-Werror=format-contains-nul"/>
    <flags REM_CXXFLAGS="-Werror=maybe-uninitialized"/>
    <flags REM_CXXFLAGS="-Werror=unused-but-set-variable"/>
    <flags REM_CXXFLAGS="-Werror=return-local-addr"/>
    <flags REM_CXXFLAGS="-fipa-pta"/>
    <flags REM_CXXFLAGS="-frounding-math"/>
    <flags REM_CXXFLAGS="-mrecip"/>
    <flags REM_CXXFLAGS="-Wno-psabi"/>
    <flags REM_CXXFLAGS="-fno-crossjumping"/>
    <flags REM_CXXFLAGS="-fno-aggressive-loop-optimizations"/>
    <flags CXXFLAGS="-Wno-c99-extensions"/>
    <flags CXXFLAGS="-Wno-c++11-narrowing"/>
    <flags CXXFLAGS="-D__STRICT_ANSI__"/>
    <flags CXXFLAGS="-Wno-unused-private-field"/>
    <flags CXXFLAGS="-Wno-unknown-pragmas"/>
    <flags CXXFLAGS="-Wno-unused-command-line-argument"/>
    <flags CXXFLAGS="-ftemplate-depth=512"/>
    <flags CXXFLAGS="-Wno-error=potentially-evaluated-expression"/>
    <flags CXXFLAGS="-O2 -pthread -pipe -Werror=main -Werror=pointer-arith"/>
    <flags CXXFLAGS="-Werror=overlength-strings -Wno-vla"/>
    <flags CXXFLAGS="-std=c++1z -ftree-vectorize -Wstrict-overflow -Werror=array-bounds -Werror=format-contains-nul -Werror=type-limits -fvisibility-inlines-hidden -fno-math-errno --param vect-max-version-for-alias-checks=50 -msse3"/>
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
    <flags LDFLAGS="-Wl,-commons -Wl,use_dylibs -Wl,-headerpad_max_install_names"/>
    <flags CXXSHAREDFLAGS="-shared -dynamic -single_module"/>
    <flags LD_UNIT=" -r "/>
    <runtime name="LD_LIBRARY_PATH" value="$$GCC_CXXCOMPILER_BASE/${LIB}" type="path"/>
    <runtime name="LD_LIBRARY_PATH" value="$$GCC_CXXCOMPILER_BASE/lib" type="path"/>
    <runtime name="PATH" value="$$GCC_CXXCOMPILER_BASE/bin" type="path"/>
  </tool>
""")
            else:
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
    <runtime name="LD_LIBRARY_PATH" value="$$GCC_CXXCOMPILER_BASE/${LIB}" type="path"/>
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
    <flags LDFLAGS="-L$$(GCC_F77COMPILER_BASE)/${LIB}"/>
    <flags LDFLAGS="-L$$(GCC_F77COMPILER_BASE)/lib"/>
    <flags FOPTIMISEDFLAGS="-O2   "/>
    <flags FSHAREDOBJECTFLAGS="-fPIC   "/>
  </tool>
""")
            write_scram_toolfile(contents, values, 'gcc-f77compiler.xml', prefix)


            contents = str("""
  <tool name="gcc-atomic" version="${GCC_VER}">
    <lib name="atomic"/>
    <client>
      <environment name="GCC_ATOMIC_BASE" default="${GCC_PREFIX}"/>
    </client>
  </tool>
""")
            write_scram_toolfile(contents, values, 'gcc-atomic.xml', prefix)
            if sys.platform == "darwin":
                contents = str("""
<tool name="root_cxxdefaults" version="6">
</tool>
""")
            else: 
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

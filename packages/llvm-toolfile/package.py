from spack import *
import sys,os,re
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class LlvmToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('llvm')
    depends_on('llvm-lib-toolfile')

    def install(self, spec, prefix):
        gcc = which(spack_f77)
        gcc_prefix = re.sub('/bin/.*$', '', self.compiler.f77)
        gcc_machine = gcc('-dumpmachine', output=str)
        gcc_ver = gcc('-dumpversion', output=str)

        values = {}
        values['VER'] = spec['llvm'].version
        values['PFX'] = spec['llvm'].prefix
        values['LIB'] = spec['llvm'].prefix.lib
        values['BIN'] = spec['llvm'].prefix.bin
        values['GCC_VER'] = gcc_ver.rstrip()
        values['GCC_PREFIX'] = gcc_prefix
        values['GCC_MACHINE'] = gcc_machine.rstrip()
        values['LDPATH_NAME'] = 'LD_LIBRARY_PATH'
        if sys.platform == 'darwin':
            values['LDPATH_NAME'] = 'DYLD_LIBRARY_PATH'

        fname='llvm-cxxcompiler.xml'
        contents = str("""<tool name="llvm-cxxcompiler" version="${VER}" type="compiler">
    <use name="gcc-cxxcompiler"/>
    <client>
      <environment name="LLVM_CXXCOMPILER_BASE" default="${PFX}"/>
      <environment name="CXX" value="clang++"/>
    </client>
    # drop flags not supported by llvm
    # -Wno-non-template-friend removed since it's not supported, yet, by llvm.
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
    <runtime name="${LDPATH_NAME}" value="${LIB}" type="path"/>
    <runtime name="PATH" value="${BIN}" type="path"/>
    <runtime name="COMPILER_RUNTIME_OBJECTS" value="${GCC_PREFIX}"/>
  </tool>""")

        write_scram_toolfile(contents,values, fname, prefix)


        fname='iwyu-cxxcompiler.xml'
        contents = str("""<tool name="iwyu-cxxcompiler" version="${VER}" type="compiler">
    <use name="llvm-cxxcompiler"/>
    <client>
      <environment name="LLVM_CXXCOMPILER_BASE" default="${PFX}"/>
      <environment name="CXX" value="${BIN}/include-what-you-use"/>
    </client>
  </tool>""")

        write_scram_toolfile(contents, values, fname, prefix)


        fname='llvm-ccompiler.xml'
        contents = str("""<tool name="llvm-ccompiler" version="${VER}" type="compiler">
    <use name="gcc-ccompiler"/>
    <client>
      <environment name="LLVM_CCOMPILER_BASE" default="${PFX}"/>
      <environment name="CC" value="clang"/>
    </client>
  </tool>""")

        write_scram_toolfile(contents, values, fname, prefix)


        fname='llvm-f77compiler.xml'
        contents = str("""  <tool name="llvm-f77compiler" version="${VER}" type="compiler">
    <use name="gcc-f77compiler"/>
    <client>
      <environment name="FC" default="gfortran"/>
    </client>
  </tool>""")

        write_scram_toolfile(contents, values, fname, prefix)


# Clang analyzer compilers
        fname='llvm-analyzer-cxxcompiler.xml'
        contents = str("""  <tool name="llvm-analyzer-cxxcompiler" version="${VER}" type="compiler">
    <use name="llvm-cxxcompiler"/>
    <client>
      <environment name="LLVM_ANALYZER_CXXCOMPILER_BASE" default="${PFX}"/>
      <environment name="CXX" value="${BIN}/c++-analyzer"/>
    </client>
    <runtime name="COMPILER_RUNTIME_OBJECTS" value="${GCC_PREFIX}"/>
  </tool>""")

        write_scram_toolfile(contents, values, fname, prefix)


        fname='llvm-analyzer-ccompiler.xml'
        contents = str("""  <tool name="llvm-analyzer-ccompiler" version="${VER}" type="compiler">
    <use name="llvm-ccompiler"/>
    <client>
      <environment name="LLVM_ANALYZER_CCOMPILER_BASE" default="${PFX}"/>
      <environment name="CC" value="${BIN}/ccc-analyzer"/>
    </client>
  </tool>""")

        write_scram_toolfile(contents, values, fname, prefix)


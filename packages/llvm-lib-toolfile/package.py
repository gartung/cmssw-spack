from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class LlvmLibToolfile(CMakePackage):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('llvm+python')

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

# This is a toolfile to use llvm / clang as a library, not as a compiler.
        fname = 'llvm.xml'
        contents = str("""  <tool name="llvm" version="${VER}">
    <lib name="clang"/>
    <client>
      <environment name="LLVM_BASE" default="${PFX}"/>
      <environment name="LIBDIR" default="${LIB}"/>
      <environment name="INCLUDE" default="${PFX}/include"/>
    </client>
    <flags LDFLAGS="-Wl,-undefined -Wl,suppress"/>
    <flags CXXFLAGS="-D_DEBUG -D_GNU_SOURCE -D__STDC_CONSTANT_MACROS"/>
    <flags CXXFLAGS="-D__STDC_FORMAT_MACROS -D__STDC_LIMIT_MACROS -O3 "/>
    <flags CXXFLAGS="-fomit-frame-pointer -fPIC -Wno-enum-compare "/>
    <flags CXXFLAGS="-Wno-strict-aliasing -fno-rtti"/>
  </tool>""")

        write_scram_toolfile(contents, values, fname, prefix)

        fname = 'pyclang.xml'
        contents = str("""<tool name="pyclang" version="${VER}">
  <client>
    <environment name="PYCLANG_BASE" default="${PFX}"/>
  </client>
  <use name="python"/>
</tool>""")

        write_scram_toolfile(contents, values, fname, prefix)

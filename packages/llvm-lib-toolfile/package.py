from spack import *
import sys,os,re
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class LlvmLibToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('llvm~gold~lldb+shared_libs+link_dylib+python')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['llvm'].version
        values['PFX'] = spec['llvm'].prefix
        values['LIB'] = spec['llvm'].prefix.lib
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

from spack import *
import sys,os,re
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class IntelTbbToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('intel-tbb')

    def install(self, spec, prefix):
        gcc = which(spack_f77)
        gcc_prefix = re.sub('/bin/.*$', '', self.compiler.f77)
        gcc_machine = gcc('-dumpmachine', output=str)
        gcc_ver = gcc('-dumpversion', output=str)
        values = {}
        values['VER'] = spec['intel-tbb'].version
        values['PFX'] = spec['intel-tbb'].prefix
        values['GCC_VER'] = gcc_ver.rstrip()
        values['GCC_GLIBCXX_VER'] = gcc_ver.rstrip().replace('.', '0')
        values['GCC_PREFIX'] = gcc_prefix
        values['GCC_MACHINE'] = gcc_machine.rstrip()
        fname = 'tbb.xml'
        contents = str("""
<tool name="tbb" version="$VER">
  <info url="http://threadingbuildingblocks.org"/>
  <lib name="tbb"/>
  <client>
    <environment name="TBB_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$TBB_BASE/lib"/>
    <environment name="INCLUDE" default="$$TBB_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <flags CPPDEFINES="TBB_USE_GLIBCXX_VERSION=$GCC_GLIBCXX_VER"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

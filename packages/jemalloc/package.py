from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile



class Jemalloc(AutotoolsPackage):
    homepage = "http://www.example.com"
    url = "https://github.com/jemalloc/jemalloc/archive/5.0.1.tar.gz"

    version('4.2.1', '25a6f63d88cabfd7f0f98a4f2f469ba7')

    depends_on('m4', type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')


    def autoreconf(self, spec, prefix):
        bash=which('bash')
        bash('autogen.sh')

    def install(self, spec, prefix):
        make()
        make('doc/jemalloc.3')
        make('doc/jemalloc.html')
        make('install')

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'jemalloc.xml'
        contents = str("""
<tool name="jemalloc" version="${VER}">
  <architecture name="slc.*|fc.*|linux*">
    <lib name="jemalloc"/>
  </architecture>
  <client>
    <environment name="JEMALLOC_BASE" default="${PFX}"/>
    <environment name="LIBDIR"        default="$$JEMALLOC_BASE/lib"/>
    <environment name="INCLUDE"        default="$$JEMALLOC_BASE/include"/>
  </client>
  <runtime name="MALLOC_CONF" value="lg_chunk:18,lg_dirty_mult:4"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <flags SKIP_TOOL_SYMLINKS="1"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)

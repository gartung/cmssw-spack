from spack import *
from contextlib import closing
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class TcmallocFake(Package):
    homepage = "http://www.example.com"
    url = "http://cmsrep.cern.ch/cmssw/cms/SOURCES/slc6_amd64_gcc600/external/google-perftools/1.6-giojec2/google-perftools-1.6.tar.gz"

    version('1.6', '7acfee8d3e2ba968d20684e9f7033015')

    def install(self, spec, prefix):
        comp = which('g++')
        with closing(open('tmpgp.cc', 'w')) as f:
            f.write("""
namespace gptmp {
  void foo(void*) {
  }
}
""")
        comp('-c', '-o', 'tmp.o', '-fPIC', 'tmpgp.cc')
        comp('-shared', '-o', 'libgptmp.so', 'tmp.o')
        mkdirp('%s' % prefix.lib)
        install('libgptmp.so', '%s/libtcmalloc.so' % prefix.lib)
        install('libgptmp.so', '%s/libtcmalloc_minimal.so' % prefix.lib)


    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'tcmalloc_minimal.xml'
        contents = str("""<tool name="tcmalloc_minimal" version="$VER">
  <lib name="tcmalloc_minimal"/>
  <client>
    <environment name="TCMALLOC_MINIMAL_BASE" default="$PFX"/>
    <environment name="LIBDIR"                default="$$TCMALLOC_MINIMAL_BASE/lib"/>
  </client>
</tool>""")

        write_scram_toolfile(contents, values, fname)

        fname = 'tcmalloc.xml'
        contents = str("""<tool name="tcmalloc" version="$VER">
  <lib name="tcmalloc"/>
  <client>
    <environment name="TCMALLOC_BASE" default="$PFX"/>
    <environment name="LIBDIR"        default="$$TCMALLOC_BASE/lib"/>
  </client>
</tool>""")

        write_scram_toolfile(contents, values, fname)

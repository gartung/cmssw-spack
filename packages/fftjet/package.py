from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Fftjet(AutotoolsPackage):


    homepage = "http://www.example.com"
    url = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/fftjet/1.5.0/fftjet-1.5.0.tar.gz"

    version('1.5.0', '9f91b6974c00ba546833c38d5b3aa563')

    depends_on('fftw')

    def configure_args(self):
        args = ['--disable-dependency-tracking',
                '--enable-threads',
                'CFLAGS=-fpic',
                'DEPS_CFLAGS=-I%s' % self.spec['fftw'].prefix.include,
                'DEPS_LIBS="-L%s -lfftw3"' % self.spec['fftw'].prefix.lib]
        return args







    @run_after('install')
    def write_scram_toolfiles(self):





        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'fftjet.xml'
        contents = str("""<tool name="fftjet" version="$VER">
  <lib name="fftjet"/>
  <client>
    <environment name="FFTJET_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$FFTJET_BASE/lib"/>
    <environment name="INCLUDE" default="$$FFTJET_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")

        write_scram_toolfile(contents, values, fname)

from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class FftjetToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand='' )
    depends_on('fftjet')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['fftjet'].version
        values['PFX'] = self.spec['fftjet'].prefix
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

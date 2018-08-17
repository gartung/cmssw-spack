from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class FftwToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=False)
    depends_on('fftw')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['fftw'].version
        values['PFX'] = self.spec['fftw'].prefix
        fname = 'fftw3.xml'
        contents = str("""
<tool name="fftw3" version="${VER}">
  <lib name="fftw3"/>
  <client>
    <environment name="FFTW3_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$FFTW3_BASE/include"/>
    <environment name="LIBDIR" default="$$FFTW3_BASE/lib"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)

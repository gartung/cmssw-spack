from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile



class HerwigToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('herwig@6.521.2')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['herwig'].version
        values['PFX'] = spec['herwig'].prefix
        fname = 'herwig.xml'
        contents = str("""
<tool name="herwig" version="${VER}">
  <lib name="herwig"/>
  <lib name="herwig_dummy"/>
  <client>
    <environment name="HERWIG_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$HERWIG_BASE/lib"/>
    <environment name="INCLUDE" default="$$HERWIG_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="f77compiler"/>
  <use name="lhapdf"/>
  <use name="photos"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

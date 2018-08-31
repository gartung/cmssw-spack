from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class ThepegToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('thepeg')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['thepeg'].version
        values['PFX'] = spec['thepeg'].prefix

        fname = 'thepeg.xml'
        contents = str("""
<tool name="thepeg" version="$VER">
  <lib name="ThePEG"/>
  <lib name="LesHouches"/>
  <client>
    <environment name="THEPEG_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$THEPEG_BASE/lib/ThePEG"/>
    <environment name="INCLUDE" default="$$THEPEG_BASE/include"/>
  </client>
  <runtime name="THEPEGPATH" value="$$THEPEG_BASE/share/ThePEG"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="lhapdf"/>
  <use name="gsl"/>
</tool>

""")

        write_scram_toolfile(contents, values, fname, prefix)

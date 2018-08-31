from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile



class HerwigppToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('herwigpp')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['herwigpp'].version
        values['PFX'] = spec['herwigpp'].prefix
        fname = 'herwigpp.xml'
        contents = str("""
<tool name="herwigpp" version="$VER">
  <lib name="HerwigAPI"/>
  <client>
    <environment name="HERWIGPP_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$HERWIGPP_BASE/lib/Herwig"/>
    <environment name="INCLUDE" default="$$HERWIGPP_BASE/include"/>
    <environment name="BINDIR" default="$$HERWIGPP_BASE/bin"/>
  </client>
  <runtime name="HERWIGPATH" value="$$HERWIGPP_BASE/share/Herwig"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <runtime name="PATH" default="$$BINDIR" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="lhapdf"/>
  <use name="thepeg"/>
  <use name="madgraph5amcatnlo"/>
  <use name="openloops"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

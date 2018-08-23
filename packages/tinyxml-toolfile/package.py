from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class TinyxmlToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('tinyxml')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['tinyxml'].version
        values['PFX'] = spec['tinyxml'].prefix

        fname = 'tinyxml.xml'
        contents = str("""<tool name="tinyxml" version="$VER">
  <info url="https://sourceforge.net/projects/tinyxml/"/>
   <lib name="tinyxml"/>
  <client>
    <environment name="TINYXML_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$TINYXML_BASE/lib"/>
    <environment name="INCLUDE" default="$$TINYXML_BASE/include"/>
  </client>  
</tool>""")

        write_scram_toolfile(contents, values, fname, prefix)

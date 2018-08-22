from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class PcreToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('pcre')

    def install(self,spec,prefix):
        values = {}
        values['VER'] = self.spec['pcre'].version
        values['PFX'] = self.spec['pcre'].prefix
        fname = 'pcre.xml'
        contents = str("""<tool name="pcre" version="$VER">
  <info url="http://www.pcre.org"/>
  <lib name="pcre"/>
  <client>
    <environment name="PCRE_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$PCRE_BASE/lib"/>
    <environment name="INCLUDE" default="$$PCRE_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="zlib"/>
  <use name="bz2lib"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

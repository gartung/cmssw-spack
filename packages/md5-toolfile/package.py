from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Md5Toolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'md5.xml'
        contents = str("""<tool name="md5" version="$VER">
  <info url="https://tls.mbed.org/md5-source-code"/>
   <lib name="cms-md5"/>
  <client>
    <environment name="MD5_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$MD5_BASE/lib"/>
    <environment name="INCLUDE" default="$$MD5_BASE/include"/>
    </client>  
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

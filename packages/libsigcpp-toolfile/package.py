from spack import *
import sys,os
import shutil
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class LibsigcppToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('libsigcpp')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['libsigcpp'].version
        values['PFX'] = spec['libsigcpp'].prefix

        shutil.copy('%s/lib/sigc++-2.0/include/sigc++config.h' % values['PFX'], 
        '%s/include/sigc++-2.0/sigc++config.h' % values['PFX'])
        fname = 'sigcpp.xml'
        contents = str("""<tool name="sigcpp" version="$VER">
  <lib name="sigc-2.0"/>
  <client>
    <environment name="SIGCPP_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$SIGCPP_BASE/lib"/>
    <environment name="INCLUDE" default="$$SIGCPP_BASE/include"/>
    <environment name="INCLUDE" default="$$SIGCPP_BASE/include/sigc++-2.0"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

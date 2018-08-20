from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class DavixToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('davix')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['davix'].version
        values['PFX'] = spec['davix'].prefix
        values['LIB'] = spec['davix'].prefix.lib64
        fname = 'davix.xml'
        contents = str("""<tool name="davix" version="$VER">
    <info url="https://dmc.web.cern.ch/projects/davix/home"/>
    <lib name="davix"/>
    <client>
      <environment name="DAVIX_BASE" default="$PFX"/>
      <environment name="LIBDIR" default="$LIB"/>
      <environment name="INCLUDE" default="$$DAVIX_BASE/include/davix"/>
    </client>
    <runtime name="PATH" value="$$DAVIX_BASE/bin" type="path"/>
    <use name="boost_system"/>
    <use name="openssl"/>
    <use name="libxml2"/>
  </tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

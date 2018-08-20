from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class XrootdToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('xrootd')

    def write_scram_toolfiles(self):
        pyvers = str(self.spec['python'].version).split('.')
        pyver = pyvers[0] + '.' + pyvers[1]

        values = {}
        values['VER'] = self.spec['xrootd'].version
        values['PFX'] = self.spec['xrootd'].prefix

        fname = 'xrootd.xml'
        contents = str("""<tool name="xrootd" version="$VER">
  <lib name="XrdUtils"/>
  <lib name="XrdClient"/>
  <client>
    <environment name="XROOTD_BASE" default="$PFX"/>
    <environment name="INCLUDE" default="$$XROOTD_BASE/include/xrootd"/>
    <environment name="INCLUDE" default="$$XROOTD_BASE/include/xrootd/private"/>
    <environment name="LIBDIR" default="$$XROOTD_BASE/lib"/>
  </client>
  <runtime name="PATH" value="$$XROOTD_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")

        write_scram_toolfile(contents, values, fname, prefix)

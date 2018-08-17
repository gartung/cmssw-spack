from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class FastjetContribToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/package.py'
    version('1.0', '', expand=True)
    depends_on('fastjet-contrib')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['fastjet-contrib'].version
        values['PFX'] = self.spec['fastjet-contrib'].prefix
        fname = 'fastjet-contrib.xml'
        contents = str("""
  <tool name="fastjet-contrib" version="${VER}">
    <info url="http://fastjet.hepforge.org/contrib/"/>
    <lib name="fastjetcontribfragile"/>
    <client>
      <environment name="FASTJET_CONTRIB_BASE" default="${PFX}"/>
      <environment name="LIBDIR" default="$$FASTJET_CONTRIB_BASE/lib"/>
      <environment name="INCLUDE" default="$$FASTJET_CONTRIB_BASE/include"/>
    </client>
  </tool>
""")

        write_scram_toolfile(contents, values, fname)

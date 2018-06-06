from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class FastjetContrib(AutotoolsPackage):
    """."""

    homepage = "http://www.example.com"
    url = "http://fastjet.hepforge.org/contrib/downloads/fjcontrib-1.014.tar.gz"

    version('1.033', git='https://github.com/cms-externals/fastjet-contrib.git', commit='69e835bfc3d36adfe70a1355a2773bc05d9f5599')

    depends_on('fastjet')

    def configure_args(self):
        args = ['--fastjet-config=%s/fastjet-config' %
                self.spec['fastjet'].prefix.bin,
                'CXXFLAGS=-I%s' % self.spec['fastjet'].prefix.include]
        return args

    def install(self, spec, prefix):
        make()
        make('check')
        make('install')
        make('fragile-shared')
        make('fragile-shared-install')

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

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

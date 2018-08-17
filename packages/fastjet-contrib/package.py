from spack import *
import sys,os


class FastjetContrib(AutotoolsPackage):

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

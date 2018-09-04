from spack import *


class Dire(AutotoolsPackage):

    url      = "https://dire.gitlab.io/Downloads/DIRE-2.002.tar.gz"

    version('2.002', sha256='7fba480bee785ddacd76446190df766d74e61a3c5969f362b8deace7d3fed8c1')

    depends_on('pythia8')

    def configure_args(self):
        args = ['--with-pythia8=%s'%self.spec['pythia8'].prefix, '--enable-shared']
        return args

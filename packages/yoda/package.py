from spack import *

class Yoda(Package):
    url = "http://cern.ch/service-spi/external/MCGenerators/distribution/yoda/yoda-1.6.5-src.tgz"
    version('1.6.5', '634fa27412730e511ca3d4c67f6086e7')
    depends_on('root')
    depends_on('py-cython', type='build')

    def install(self, spec, prefix):
        with working_dir(str(self.spec.version), create=False):
            configure('--enable-root', '--prefix=%s' % self.prefix)
            make('all')
            make('install')

from spack import *
import sys,os,glob
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Libpython2(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)

    depends_on('python@:2.7.99', type='build')

    def install(self, spec, prefix):
        install_tree( '%s/python2.7' %
                       spec['python'].prefix.include,
                      '%s/python2.7' %
                     self.prefix.include)
        mkdirp(self.prefix.lib)
        for f in glob.glob('%s/libpython*' % self.spec['python'].prefix.lib):
            install(f, self.prefix.lib+'/'+os.path.basename(f))

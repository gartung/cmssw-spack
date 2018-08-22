from spack import *
import glob
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Libhepml(Package):
    homepage = "http://www.example.com"
    url = "http://mcdb.cern.ch/distribution/api/libhepml-0.2.1.tar.gz"

    version('0.2.6',    'e414906a3e475cd7e5bdb6119fea15c1')
    version('0.2.5',    'c34d2155002f47de76728516a940f881')
    version('0.2.3ext', 'c17ea60f8bf93bfea7cc14bb57b0a0a1')
    version('0.2.3',    '29120e56c2bcbd59425fee82f7fdb5a1')
    version('0.2.2',    '76f3d5458252e67476dd661685e9983d')
    version('0.2.1',    '646964f8478fe0d64888514a8a1d8d19', preferred=True)

    patch('libhepml-0.2.1-gcc43.patch', level=2)

    def install(self, spec, prefix):
        mkdirp(prefix.lib)
        with working_dir('src'):
            make()
            for f in glob.glob('*.so'):
                install(f, join_path(prefix.lib, f))
        install_tree('interface', join_path(prefix, 'interface'))


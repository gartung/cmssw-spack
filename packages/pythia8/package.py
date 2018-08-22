from spack import *
import os
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Pythia8(Package):
    """Event generator pythia"""

    homepage = "http://home.thep.lu.se/~torbjorn/Pythia.html"
    url = "http://home.thep.lu.se/~torbjorn/pythia8/pythia8219.tgz"

    depends_on('hepmc')
    depends_on('lhapdf')

    version('230', git='https://github.com/cms-externals/pythia8.git', 
            commit='6e0f72a4478754a4fb13c91ccc92f21947f2788e')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  '--enable-shared',
                  '--with-hepmc2=%s' % spec['hepmc'].prefix,
                  '--with-lhapdf6=%s' % spec['lhapdf'].prefix )
        make('-j4', 'VERBOSE=1')
        make("install")

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('PYTHIA8_DIR', self.prefix)
        spack_env.set('PYTHIA8_XML', os.path.join(
            self.prefix, "share", "Pythia8", "xmldoc"))
        spack_env.set('PYTHIA8DATA', os.path.join(
            self.prefix, "share", "Pythia8", "xmldoc"))

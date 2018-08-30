from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Eigen(CMakePackage):
    """Eigen is a C++ template library for linear algebra matrices,
    vectors, numerical solvers, and related algorithms.
    """

    homepage = 'http://eigen.tuxfamily.org/'
    url='https://github.com/cms-externals/eigen-git-mirror/archive/1ae2849542a7892089f81f2ee460b510cdb0a16d.tar.gz'

    version('64060da8461a627eb25b5a7bc0616776068db58b',git='https://github.com/cms-externals/eigen-git-mirror',
            commit='64060da8461a627eb25b5a7bc0616776068db58b')

    variant('metis', default=False, description='Enables metis backend')
    variant('scotch', default=False, description='Enables scotch backend')
    variant('fftw', default=False, description='Enables FFTW backend')
    variant('suitesparse', default=False,
            description='Enables SuiteSparse support')
    variant('mpfr', default=False,
            description='Enables support for multi-precisions FP via mpfr')
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo'))

    # TODO : dependency on googlehash, superlu, adolc missing
    depends_on('metis@5:', when='+metis')
    depends_on('scotch', when='+scotch')
    depends_on('fftw', when='+fftw')
    depends_on('suite-sparse', when='+suitesparse')
    depends_on('mpfr@2.3.0:', when='+mpfr')
    depends_on('gmp', when='+mpfr')

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('EIGEN_SOURCE','https://github.com/cms-externals/eigen-git-mirror/archive/%s.tar.gz' % self.version)
        spack_env.set('EIGEN_STRIP_PREFIX','eigen-git-mirror-%s'%self.version)

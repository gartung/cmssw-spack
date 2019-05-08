from spack import *
import platform
import sys,os

class Geant4(CMakePackage):
    """Geant4 is a toolkit for the simulation of the passage of particles
    through matter. Its areas of application include high energy, nuclear
    and accelerator physics, as well as studies in medical and space
    science."""

    homepage = "http://geant4.cern.ch/"
    url = "http://geant4.cern.ch/support/source/geant4.10.01.p03.tar.gz"

    version('10.04', git='https://github.com/cms-externals/geant4.git', commit='7788cfbecfee824344bd3761cb32efe2bdc53046')
    version('10.02.p02', '6aae1d0fc743b0edc358c5c8fbe48657')

    variant('qt', default=False, description='Enable Qt support')
    variant('vecgeom', default=True, description='Enable Vecgeom support')

    depends_on('cmake@3.5:', type='build')

    depends_on("clhep")
    depends_on("expat")
    depends_on("zlib")
    depends_on("xerces-c")
    depends_on("qt@4.8:", when="+qt")
    depends_on("vecgeom", when="+vecgeom")
    # G4 data
    depends_on("geant4-g4emlow")
    depends_on("geant4-g4ndl")
    depends_on("geant4-g4photonevaporation")
    depends_on("geant4-g4saiddata")
    depends_on("geant4-g4abla")
    depends_on("geant4-g4ensdfstate")
    depends_on("geant4-g4neutronsxs")
    depends_on("geant4-g4radioactivedecay")

    def cmake_args(self):
        spec = self.spec
        dso_suffix="so"
        if sys.platorm == "darwin":
            dso_suffix="dylib"
        options = [ '-DCMAKE_CXX_COMPILER=g++'
                   ,'-DCMAKE_CXX_FLAGS=-fPIC'
                   ,'-DCMAKE_INSTALL_LIBDIR=lib'
                   ,'-DCMAKE_BUILD_TYPE=Release'
                   ,'-DGEANT4_USE_GDML=ON'
                   ,'-DGEANT4_BUILD_CXXSTD:STRING=c++14'
                   ,'-DGEANT4_BUILD_TLS_MODEL:STRING=global-dynamic'
                   ,'-DGEANT4_ENABLE_TESTING=OFF'
                   ,'-DGEANT4_BUILD_VERBOSE_CODE=OFF'
                   ,'-DBUILD_SHARED_LIBS=ON'
                   ,'-DXERCESC_ROOT_DIR:PATH=%s' %
                     spec['xerces-c'].prefix
                   ,'-DCLHEP_ROOT_DIR:PATH=%s' %
                     spec['clhep'].prefix
                   ,'-DEXPAT_INCLUDE_DIR:PATH=%s' %
                     spec['expat'].prefix.include
                   ,'-DEXPAT_LIBRARY:FILEPATH=%s/libexpat.%s' % 
                     (spec['expat'].prefix.lib, dso_suffix)
                   ,'-DBUILD_STATIC_LIBS=ON'
                   ,'-DGEANT4_INSTALL_EXAMPLES=OFF'
                   ,'-DGEANT4_USE_SYSTEM_CLHEP=ON'
                   ,'-DGEANT4_BUILD_MULTITHREADED=ON'
                   ,'-DCMAKE_STATIC_LIBRARY_CXX_FLAGS=-fPIC'
                   ,'-DCMAKE_STATIC_LIBRARY_C_FLAGS=-fPIC' ]

        if '+vecgeom' in spec:
            options.append('-DGEANT4_USE_USOLIDS=ON')
            options.append('-DUSolids_DIR=%s' %
                           join_path(spec['vecgeom'].prefix, 'lib/CMake/USolids'))

        arch = platform.system().lower()
        if arch is not 'darwin':
            options.append('-DGEANT4_USE_OPENGL_X11=ON')
            options.append('-DGEANT4_USE_XM=ON')
            options.append('-DGEANT4_USE_RAYTRACER_X11=ON')

        if '+qt' in spec:
            options.append('-DGEANT4_USE_QT=ON')
            options.append(
                '-DQT_QMAKE_EXECUTABLE=%s' %
                spec['qt'].prefix + '/bin/qmake'
            )

        return options

    def url_for_version(self, version):
        """Handle Geant4's unusual version string."""
        return ("http://geant4.cern.ch/support/source/geant4.%s.tar.gz" % version)


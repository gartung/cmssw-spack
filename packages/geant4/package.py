from spack import *
import platform
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


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

    depends_on("clhep~cxx11+cxx14")
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

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['GEANT4_VER'] = self.spec.version
        values['GEANT4_PREFIX'] = self.spec.prefix

        fname = 'geant4.xml'
        contents = str("""
<tool name="geant4" version="${GEANT4_VER}">
  <info url="http://geant4.web.cern.ch/geant4/"/>
  <use name="geant4core"/>
  <use name="geant4vis"/>
  <use name="xerces-c"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)

        fname = 'geant4core.xml'
        contents = str("""
<tool name="geant4core" version="${GEANT4_VER}">
  <info url="http://geant4.web.cern.ch/geant4/"/>
  <lib name="G4digits_hits"/>
  <lib name="G4error_propagation"/>
  <lib name="G4event"/>
  <lib name="G4geometry"/>
  <lib name="G4global"/>
  <lib name="G4graphics_reps"/>
  <lib name="G4intercoms"/>
  <lib name="G4interfaces"/>
  <lib name="G4materials"/>
  <lib name="G4parmodels"/>
  <lib name="G4particles"/>
  <lib name="G4persistency"/>
  <lib name="G4physicslists"/>
  <lib name="G4processes"/>
  <lib name="G4readout"/>
  <lib name="G4run"/>
  <lib name="G4tracking"/>
  <lib name="G4track"/>
  <lib name="G4analysis"/>
  <flags CXXFLAGS="-DG4MULTITHREADED -DG4USE_STD11 -ftls-model=global-dynamic -pthread"/>
  <client>
    <environment name="GEANT4_BASE" default="${GEANT4_PREFIX}"/>
    <environment name="LIBDIR" default="$$GEANT4_BASE/lib"/>
    <environment name="G4LIB" value="$$LIBDIR"/>
    <environment name="INCLUDE" default="$$GEANT4_BASE/include/Geant4"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH"  value="$$INCLUDE" type="path"/>
  <flags cppdefines="GNU_GCC G4V9"/>
  <use name="clhep"/>
  <use name="root_cxxdefaults"/>
  <flags SKIP_TOOL_SYMLINKS="1"/>
</tool>
""")


        write_scram_toolfile(contents, values, fname)

        fname = 'geant4data.xml'
        contents = str("""
<tool name="geant4data" version="${GEANT4_VER}">
  <use name="geant4data_g4abla"/>
  <use name="geant4data_g4emlow"/>
  <use name="geant4data_g4ensdfstate"/>
  <use name="geant4data_g4ndl"/>
  <use name="geant4data_g4neutronsxs"/>
  <use name="geant4data_g4photonevaporation"/>
  <use name="geant4data_g4radioactivedecay"/>
  <use name="geant4data_g4saiddata"/>
</tool>
""")


        write_scram_toolfile(contents, values, fname)

        fname = 'geant4vis.xml'
        contents = str("""
<tool name="geant4vis" version="${GEANT4_VER}">
  <info url="http://geant4.web.cern.ch/geant4/"/>
  <lib name="G4FR"/>
  <lib name="G4modeling"/>
  <lib name="G4RayTracer"/>
  <lib name="G4Tree"/>
  <lib name="G4visHepRep"/>
  <lib name="G4vis_management"/>
  <lib name="G4visXXX"/>
  <lib name="G4VRML"/>
  <lib name="G4GMocren"/>
  <lib name="G4zlib"/>
  <use name="geant4core"/>
</tool>
""")


        write_scram_toolfile(contents, values, fname)

from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Clhep(CMakePackage):
    """CLHEP is a C++ Class Library for High Energy Physics. """
    homepage = "http://proj-clhep.web.cern.ch/proj-clhep/"
    url      = "http://proj-clhep.web.cern.ch/proj-clhep/DISTRIBUTION/tarFiles/clhep-2.2.0.5.tgz"
    list_url = "https://proj-clhep.web.cern.ch/proj-clhep/"
    list_depth = 1

    version('2.4.0.4', 'e1c48324507e5be41d76772a14eff242')
    version('2.4.0.2', '5e11db4d696f0654334369d17c71e42a')
    version('2.4.0.1', 'f06aa2924abbfee0afd5a9beaaa883cf')
    version('2.4.0.0', '9af6644e4e04d6807f53956512b7396a')
    version('2.3.4.6', 'a38bf1b5bb36901214b46b209d4a4c66')
    version('2.3.4.5', '31b4785b40706ff7503bb9ffd412487a')
    version('2.3.4.4', '8b8a33d0d19213b60d6c22ce5fc93761')
    version('2.3.4.3', '6941279f70d69492fff1aa955f3f2562')
    version('2.3.4.2', '1e7a9046c9ad0b347d6812f8031191da')
    version('2.3.4.1', '5ae85571ff3d8b2c481c3f95ea89b751')
    version('2.3.4.0', 'dd899d0791a823221927f97edf190348')
    version('2.3.3.2', '8b9f8d7f4dccec6d058b3a078f66b6a3')
    version('2.3.3.1', '456ef9d262ef4e776af984bfbe2f48c7')
    version('2.3.3.0', '3637eaa6750606e589e52c9e155a382e')
    version('2.3.2.2', '567b304b0fa017e1e9fbf199f456ebe9')
    version('2.3.2.1', '064903cb5c23b54f520d04ca6230b901')
    version('2.3.1.1', '16efca7641bc118c9d217cc96fe90bf5')
    version('2.3.1.0', 'b084934fc26a4182a08c09c292e19161')
    version('2.3.0.0', 'a00399a2ca867f2be902c22fc71d7e2e')
    version('2.2.0.8', '5a23ed3af785ac100a25f6cb791846af')
    version('2.2.0.5', '1584e8ce6ebf395821aed377df315c7c')
    version('2.2.0.4', '71d2c7c2e39d86a0262e555148de01c1')

    variant('cxx11', default=False, description="Compile using c++11 dialect.")
    variant('cxx14', default=False, description="Compile using c++14 dialect.")
    variant('cxx17', default=True, description="Compile using c++17 dialect.")

    depends_on('cmake@2.8.12.2:', when='@2.2.0.4:2.3.0.0', type='build')
    depends_on('cmake@3.2:', when='@2.3.0.1:', type='build')

    def patch(self):
        filter_file('SET CMP0042 OLD',
                    'SET CMP0042 NEW',
                    '%s/%s/CLHEP/CMakeLists.txt'
                    % (self.stage.path, self.spec.version))

    root_cmakelists_dir = 'CLHEP'

    def cmake_args(self):
        spec = self.spec
        cmake_args = []

        if '+cxx11' in spec:
            if 'CXXFLAGS' in env and env['CXXFLAGS']:
                env['CXXFLAGS'] += ' ' + self.compiler.cxx11_flag
            else:
                env['CXXFLAGS'] = self.compiler.cxx11_flag
            cmake_args.append('-DCLHEP_BUILD_CXXSTD=' +
                              self.compiler.cxx11_flag)

        if '+cxx14' in spec:
            if 'CXXFLAGS' in env and env['CXXFLAGS']:
                env['CXXFLAGS'] += ' ' + self.compiler.cxx14_flag
            else:
                env['CXXFLAGS'] = self.compiler.cxx14_flag
            cmake_args.append('-DCLHEP_BUILD_CXXSTD=' +
                              self.compiler.cxx14_flag)
        if '+cxx17' in spec:
            if 'CXXFLAGS' in env and env['CXXFLAGS']:
                env['CXXFLAGS'] += ' ' + self.compiler.cxx17_flag
            else:
                env['CXXFLAGS'] = self.compiler.cxx17_flag
            cmake_args.append('-DCLHEP_BUILD_CXXSTD=' +
                              self.compiler.cxx17_flag)

        return cmake_args

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'clhep.xml'
        contents = str("""<tool name="clhep" version="$VER">
  <info url="http://wwwinfo.cern.ch/asd/lhc++/clhep"/>
  <lib name="CLHEP"/>
  <client>
    <environment name="CLHEP_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$CLHEP_BASE/lib"/>
    <environment name="INCLUDE" default="$$CLHEP_BASE/include"/>
  </client>
  <runtime name="CLHEP_PARAM_PATH" value="$$CLHEP_BASE"/>
  <runtime name="CMSSW_FWLITE_INCLUDE_PATH" value="$$CLHEP_BASE/include" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <flags CXXFLAGS="-Wno-error=unused-variable"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)

        fname = 'clhepheader.xml'
        contents = str("""<tool name="clhepheader" version="$VER">
  <info url="http://wwwinfo.cern.ch/asd/lhc++/clhep"/>
  <client>
    <environment name="CLHEPHEADER_BASE" default="$PFX"/>
    <environment name="INCLUDE"    default="$$CLHEPHEADER_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH"  value="$$INCLUDE" type="path"/>
  <flags CXXFLAGS="-Wno-error=unused-variable"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)

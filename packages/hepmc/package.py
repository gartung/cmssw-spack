from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Hepmc(Package):
    """The HepMC package is an object oriented, C++ event record for
       High Energy Physics Monte Carlo generators and simulation."""

    homepage = "http://hepmc.web.cern.ch/hepmc/"
    url = "http://lcgapp.cern.ch/project/simu/HepMC/download/HepMC-2.06.09.tar.gz"

    version('2.06.09', 'c47627ced4255b40e731b8666848b087')
    version('2.06.08', 'a2e889114cafc4f60742029d69abd907')
    version('2.06.07', '11d7035dccb0650b331f51520c6172e7')

    depends_on("cmake", type='build')

    def install(self, spec, prefix):
        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path
        options = [source_directory]
        options.append('-Dmomentum:STRING=GEV')
        options.append('-Dlength:STRING=MM')
        options.extend(std_cmake_args)

        with working_dir(build_directory, create=True):
            cmake(*options)
            make()
            make('install')
            fix_darwin_install_name(prefix.lib)

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.prepend_path('LD_LIBRARY_PATH', self.prefix.lib)
    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'hepmc.xml'
        contents = str("""<tool name="HepMC" version="$VER">
  <lib name="HepMCfio"/>
  <lib name="HepMC"/>
  <client>
    <environment name="HEPMC_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$HEPMC_BASE/lib"/>
  </client>
  <use name="hepmc_headers"/>
  <runtime name="CMSSW_FWLITE_INCLUDE_PATH" value="$$HEPMC_BASE/include" type="path"/>
</tool>""")

        write_scram_toolfile(contents, values, fname)

        fname = 'hepmc_headers.xml'
        contents = str("""<tool name="hepmc_headers" version="$VER">
  <client>
    <environment name="HEPMC_HEADERS_BASE" default="$PFX"/>
    <environment name="INCLUDE" default="$$HEPMC_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH"  value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")

        write_scram_toolfile(contents, values, fname)

from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile



class Heppdt(AutotoolsPackage):
    """The HepPID library contains translation methods for particle ID's
    to and from various Monte Carlo generators and the PDG standard
    numbering scheme. We realize that the generators adhere closely
    to the standard, but there are occasional differences."""
    homepage = "http://lcgapp.cern.ch/project/simu/HepPDT/"
    url = "http://lcgapp.cern.ch/project/simu/HepPDT/download/HepPDT-2.06.01.tar.gz"

    version('3.04.01', 'a8e93c7603d844266b62d6f189f0ac7e')
    version('3.04.00', '2d2cd7552d3e9539148febacc6287db2')
    version('3.03.02', '0b85f1809bb8b0b28a46f23c718b2773')
    version('3.03.01', 'd411f3bfdf9c4350d802241ba2629cc2')
    version('3.03.00', 'cd84d0a0454be982dcd8c285e060a7b3')
    version('2.06.01', '5688b4bdbd84b48ed5dd2545a3dc33c0')

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.prepend_path('LD_LIBRARY_PATH', self.prefix.lib)

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'heppdt.xml'
        contents = str("""
<tool name="heppdt" version="${VER}">
  <lib name="HepPDT"/>
  <lib name="HepPID"/>
  <client>
    <environment name="HEPPDT_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$HEPPDT_BASE/lib"/>
    <environment name="INCLUDE" default="$$HEPPDT_BASE/include"/>
  </client>
  <runtime name="HEPPDT_PARAM_PATH" value="$$HEPPDT_BASE"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <flags SKIP_TOOL_SYMLINKS="1"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)

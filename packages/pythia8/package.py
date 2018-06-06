from spack import *
import os
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Pythia8(Package):
    """Event generator pythia"""

    homepage = "http://home.thep.lu.se/~torbjorn/Pythia.html"
    url = "http://home.thep.lu.se/~torbjorn/pythia8/pythia8219.tgz"

    version('8219', '3459b52b5da1deae52cbddefa6196feb')
    version('8215', 'b4653133e6ab1782a5a4aa66eda6a54b')
    version('8212', '0886d1b2827d8f0cd2ae69b925045f40')
    version('8210', '685d61f08ca486caa6d5dfa35089e4ab')
    version('8209', '1b9e9dc2f8a2c2db63bce739242fbc12')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('PYTHIA8_DIR', self.prefix)
        spack_env.set('PYTHIA8_XML', os.path.join(
            self.prefix, "share", "Pythia8", "xmldoc"))
        spack_env.set('PYTHIA8DATA', os.path.join(
            self.prefix, "share", "Pythia8", "xmldoc"))

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'pythia8.xml'
        contents = str("""
<tool name="pythia8" version="${VER}">
  <lib name="pythia8"/>
  <client>
    <environment name="PYTHIA8_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$PYTHIA8_BASE/lib"/>
    <environment name="INCLUDE" default="$$PYTHIA8_BASE/include"/>
  </client>
  <runtime name="PYTHIA8DATA" value="$$PYTHIA8_BASE/share/Pythia8/xmldoc"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="cxxcompiler"/>
  <use name="hepmc"/>
  <use name="lhapdf"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)

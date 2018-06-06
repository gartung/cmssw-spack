from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Libsigcpp(Package):
    """Description"""

    homepage = "http://www.example.com"
    url = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/sigcpp/2.6.2/libsigc++-2.6.2.tar.xz"

    version('2.6.2', 'd2f33ca0b4b012ef60669e3b3cebe956')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
        cp = which('cp')
        cp(prefix + '/lib/sigc++-2.0/include/sigc++config.h',
           prefix + '/include/sigc++-2.0/')

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'sigcpp.xml'
        contents = str("""<tool name="sigcpp" version="$VER">
  <lib name="sigc-2.0"/>
  <client>
    <environment name="SIGCPP_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$SIGCPP_BASE/lib"/>
    <environment name="INCLUDE" default="$$SIGCPP_BASE/include/sigc++-2.0"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")

        write_scram_toolfile(contents, values, fname)

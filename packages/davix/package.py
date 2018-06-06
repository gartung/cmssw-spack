from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Davix(CMakePackage):


    homepage = "http://www.example.com"
    url = "https://github.com/cern-it-sdc-id/davix/archive/R_0_6_5.tar.gz"

    version('0_6_5', 'a7f09dfa0bd0daaa46aafc8e0f4b1a25')

    depends_on('libxml2+python')
    depends_on('boost+python')
    depends_on('cmake', type='build')

    def cmake_args(self):
        args = ['-DLIBXML2_INCLUDE_DIR=%s/include/libxml2' % self.spec['libxml2'].prefix,
                '-DLIBXML2_LIBRARIES=%s/lib/libxml2.%s' %
                (self.spec['libxml2'].prefix, dso_suffix),
                '-DBoost_NO_SYSTEM_PATHS:BOOL=TRUE',
                '-DBOOST_ROOT:PATH=%s' % self.spec['boost'].prefix,
                '-DOPENSSL_ROOT_DIR=%s' % self.spec['openssl'].prefix]
        return args

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix
        values['LIB'] = self.spec.prefix.lib64

        fname = 'davix.xml'
        contents = str("""<tool name="davix" version="$VER">
    <info url="https://dmc.web.cern.ch/projects/davix/home"/>
    <lib name="davix"/>
    <client>
      <environment name="DAVIX_BASE" default="$PFX"/>
      <environment name="LIBDIR" default="$LIB"/>
      <environment name="INCLUDE" default="$$DAVIX_BASE/include/davix"/>
    </client>
    <runtime name="PATH" value="$$DAVIX_BASE/bin" type="path"/>
    <use name="boost_system"/>
    <use name="openssl"/>
    <use name="libxml2"/>
  </tool>""")
        write_scram_toolfile(contents, values, fname)

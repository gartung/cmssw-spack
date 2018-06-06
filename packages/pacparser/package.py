from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Pacparser(Package):
    homepage = "http://www.example.com"
    url = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/pacparser/1.3.5/pacparser-1.3.5.tar.gz"

    version('1.3.5', '9db90bd4d88dfd8d31fa707466259566')

    def install(self, spec, prefix):
        make('-C', 'src', 'PREFIX=%s' % prefix, 'CXXFLAGS=-Wno-unused-but-set-variable')
        make('-C', 'src', 'install', 'PREFIX=%s' % prefix)


    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'pacparser.xml'
        contents = str("""<tool name="pacparser" version="$VER">
  <info url="http://code.google.com/p/pacparser/"/>
  <lib name="pacparser"/>
  <client>
    <environment name="PACPARSER_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$PACPARSER_BASE/lib"/>
    <environment name="INCLUDE" default="$$PACPARSER_BASE/include"/>
  </client>
  <runtime name="PATH" value="$$PACPARSER_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")

        write_scram_toolfile(contents, values, fname)

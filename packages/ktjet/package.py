from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Ktjet(AutotoolsPackage):
    homepage = "http://www.example.com"
    url      = "http://www.hepforge.org/archive/ktjet/KtJet-1.0.6.tar.gz"

    version('1.06', '44294e965734da8844395c446a813d7e')

    depends_on('clhep')

    patch('ktjet-1.0.6-nobanner.patch')

    def configure_args(self):

        args = ['--with-clhep=%s'%self.spec['clhep'].prefix,
                'CPPFLAGS=-DKTDOUBLEPRECISION -fPIC']
        return args


    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'ktjet.xml'
        contents = str("""
<tool name="ktjet" version="${VER}">
  <info url="http://hepforge.cedar.ac.uk/ktjet"/>
  <lib name="KtEvent"/>
  <client>
    <environment name="KTJET_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$KTJET_BASE/lib"/>
    <environment name="INCLUDE" default="$$KTJET_BASE/include"/>
  </client>
  <flags cppdefines="KTDOUBLEPRECISION"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <flags SKIP_TOOL_SYMLINKS="1"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)


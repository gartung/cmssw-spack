from spack import *
import glob
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile



class Hector(Package):
    homepage = "http://www.example.com"
    url = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/hector/1.3.4_patch1-fmblme3/hector-1.3.4_patch1.tgz"
    depends_on('root')

    version('1.3.4_patch1', '419ec3ce8dfbcff972ea6d5b09e8c6f1')

    def install(self, spec, prefix):
        mkdirp('obj')
        mkdirp('lib')
        make()
        cp = which('cp')
        for f in glob.glob('*'):
            cp('-r', f, prefix)

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'hector.xml'
        contents = str("""
<tool name="Hector" version="${VER}">
  <info url="http://www.fynu.ucl.ac.be/themes/he/ggamma/hector/"/>
  <lib name="Hector"/>
  <client>
    <environment name="HECTOR_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$HECTOR_BASE/lib"/>
    <environment name="INCLUDE" default="$$HECTOR_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)

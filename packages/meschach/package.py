from spack import *
import glob
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Meschach(Package):
    homepage = "http://www.example.com"
    url = "http://homepage.divms.uiowa.edu/~dstewart/meschach/mesch12b.tar.gz"

    version('12b', '4ccd520f30934ebc34796d80dab29e5c')

    patch('meschach-1.2b-fPIC.patch', level=0)
    patch('meschach-1.2-slc4.patch')

    def install(self, spec, prefix):
        make('all')
        mkdirp(prefix.lib)
        mkdirp(prefix.include)
        for f in glob.glob('*.h'):
            install(f, prefix.include + '/' + f)
        install('meschach.a', prefix.lib + '/libmeschach.a')


    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'meschach.xml'
        contents = str("""<tool name="meschach" version="$VER">
  <info url="http://www.meschach.com"/>
  <lib name="meschach"/>
  <client>
    <environment name="MESCHACH_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$MESCHACH_BASE/lib"/>
    <environment name="INCLUDE" default="$$MESCHACH_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")

        write_scram_toolfile(contents, values, fname)

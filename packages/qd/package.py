from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Qd(Package):
    homepage = "http://www.example.com"
    url      = "http://crd.lbl.gov/~dhbailey/mpdist/qd-2.3.13.tar.gz"
    
    version('2.3.18', '48e788826c0c610f4f0eb49e5465a32b')


    def patch(self):
        os.remove('./config/config.sub')
        os.remove('./config/config.guess')
        install(join_path(os.path.dirname(__file__), '../../config.sub'), './config/config.sub')
        install(join_path(os.path.dirname(__file__), '../../config.guess'), './config/config.guess')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix,
                  '--enable-shared')
        make()
        make('install')

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'qd.xml'
        contents = str("""
<tool name="qd" version="${VER}">
<lib name="qd_f_main"/>
<lib name="qdmod"/>
<lib name="qd"/>
<client>
<environment name="QD_BASE" default="${PFX}"/>
<environment name="LIBDIR" default="$$QD_BASE/lib"/>
<environment name="INCLUDE" default="$$QD_BASE/include"/>
</client>
</tool>
""")
        write_scram_toolfile(contents, values, fname)

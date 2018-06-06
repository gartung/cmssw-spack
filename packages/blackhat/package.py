from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile

class Blackhat(Package):



    homepage = "http://www.example.com"
    url      = "http://www.hepforge.org/archive/blackhat/blackhat-0.9.9.tar.gz"

    version('0.9.9', '64a4e64a95754bb701bf0c1f88c8ee53')

    patch('blackhat-gcc48.patch')
#    patch('blackhat-0.9.9-armv7hl.patch')
    patch('blackhat-no_warnings.patch')
    patch('blackhat-0.9.9-default-arg-at-first-decl.patch')
    patch('blackhat-0.9.9-gcc600.patch')



    depends_on('qd')
    depends_on('openssl')
    depends_on('python')

    def patch(self):
        if os.path.exists('./config/config.sub'):
            os.remove('./config/config.sub')
            install(join_path(os.path.dirname(__file__), '../../config.sub'), './config/config.sub')
        if os.path.exists('./config/config.guess'):
            os.remove('./config/config.guess')
            install(join_path(os.path.dirname(__file__), '../../config.guess'), './config/config.guess')



    def install(self, spec, prefix):
        QD_ROOT=spec['qd'].prefix
        OPENSSL_ROOT=spec['openssl'].prefix
        configure('--prefix=%s' % prefix,
                '--with-QDpath=%s' % QD_ROOT,
                'CXXFLAGS=-Wno-deprecated -I%s/include' % OPENSSL_ROOT,
                'LDFLAGS=-L%s/lib' % OPENSSL_ROOT)
        make()
        make('install')


    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'blackhat.xml'
        contents = str("""
<tool name="blackhat" version="${VER}">
<lib name="Ampl_eval"/>
<lib name="BG"/>
<lib name="BH"/>
<lib name="BHcore"/>
<lib name="CutPart"/>
<lib name="Cut_wCI"/>
<lib name="Cuteval"/>
<lib name="Integrals"/>
<lib name="Interface"/>
<lib name="OLA"/>
<lib name="RatPart"/>
<lib name="Rateval"/>
<lib name="Spinors"/>
<lib name="assembly"/>
<lib name="ratext"/>
<client>
<environment name="BLACKHAT_BASE" default="${PFX}"/>
<environment name="LIBDIR" default="$$BLACKHAT_BASE/lib/blackhat"/>
<environment name="INCLUDE" default="$$BLACKHAT_BASE/include"/>
</client>
<use name="qd"/>
<runtime name="WORKER_DATA_PATH" value="$$BLACKHAT_BASE/share/blackhat/datafiles/" type="path"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)


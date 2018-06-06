from spack import *
import glob
import shutil
import distutils.dir_util as du
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile



class Tauola(Package):
    homepage = "http://www.example.com"
    url      = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/tauola/tauola-28.121.2-src.tgz"

    #version('28.121.2', '275ec7dd7ce9c091c042c033a434754d')
    #version('28.121',   'e2c75a6e566c98f3972744883f687b9c')
    version('27.121.5', 'b0a155d16ea5759701636202d1f6de3e')

    depends_on('pythia6')
    depends_on('photos')


    patch('tauola-27.121.5-gfortran-taueta.patch')
    patch('tauola-27.121-gfortran-tauola-srs.patch')
    patch('tauola-27.121.5-configure-makefile-update.patch')


    def install(self, spec, prefix):
        cmsplatf=spec.architecture
        with working_dir(self.version.string):
            filter_file('hepevt.inc', '../include/hepevt.inc', './pretauola/tauola_srs.F')
            filter_file('hepevt.inc', '../include/hepevt.inc', './pretauola/itldrc.F')
            filter_file('hepevt.inc', '../include/hepevt.inc', './pretauola/pyhepc_t.F')
            perl=which('perl')
            perl('-p', '-i', '-e', 
                's|-fno-globals||g;s|-finit-local-zero||g;'+
                's|-fugly-logint||g;s|-fugly-complex||',
                'configure')
            configure('--lcgplatform=%s' % cmsplatf,
                      '--with-pythia6libs=%s' % spec['pythia6'].prefix.lib)
            make('PHOTOS=%s' % spec['photos'].prefix)
            du.copy_tree('lib',prefix.lib)
            du.copy_tree('include',prefix.include)
            for f in glob.glob(prefix.lib+'/archive/*.a'):
                shutil.move(f,join_path(prefix.lib,os.path.basename(f)))
            shutil.rmtree(prefix.lib+'/archive')

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'tauola.xml'
        contents = str("""
<tool name="tauola" version="${VER}">
  <lib name="pretauola"/>
  <lib name="tauola"/>
  <client>
    <environment name="TAUOLA_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$TAUOLA_BASE/lib"/>
  </client>
  <use name="f77compiler"/>
  <use name="tauola_headers"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)

        fname = 'tauola_headers.xml'
        contents = str("""
<tool name="tauola_headers" version="${VER}">
  <client>
    <environment name="TAUOLA_HEADERS_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$TAUOLA_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)

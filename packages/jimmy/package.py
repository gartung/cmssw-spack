from spack import *
import  distutils.dir_util as du
import  distutils.file_util as fu
import glob
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Jimmy(Package):
    homepage = "http://www.example.com"
    url      = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/jimmy/jimmy-4.2-src.tgz"
    
    version('4.2', '940ca1c4404cb13d42c99986597dd57e')

    depends_on('herwig')
 
    patch('jimmy-4.2-configure-update.patch')

    def install(self, spec, prefix):
        with working_dir(str(self.version)):
            configure('--with-herwig=%s' % spec['herwig'].prefix)
            make('HERWIG_ROOT=%s' % spec['herwig'].prefix, 'lib_archive')
            du.copy_tree('include', prefix.include)
            du.copy_tree('lib', prefix.lib)
            for f in glob.glob(prefix.lib+'/archive/*.a'):
                fu.move_file(f,prefix.lib)
                du.remove_tree(prefix.lib+'/archive')

    def url_for_version(self,version):
        url='http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/jimmy/jimmy-%s-src.tgz'%version
        return url

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'jimmy.xml'
        contents = str("""
<tool name="jimmy" version="${VER}">
  <lib name="jimmy"/>
  <client>
    <environment name="JIMMY_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$JIMMY_BASE/lib"/>
  </client>
  <use name="f77compiler"/>
  <use name="herwig"/>
  <use name="jimmy_headers"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)

        fname = 'jimmy_headers.xml'
        contents = str("""
<tool name="jimmy_headers" version="${VER}">
  <client>
    <environment name="JIMMY_HEADERS_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$JIMMY_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)


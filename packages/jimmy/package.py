from spack import *
import  distutils.dir_util as du
import  distutils.file_util as fu
import glob
import sys,os


class Jimmy(Package):

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


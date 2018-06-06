from spack import *
import glob
import shutil
import distutils.dir_util as du
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile

class Photos(Package):
    homepage = "http://www.example.com"
    url = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/photos/photos-215.5-src.tgz"

    version('215.5', '87bc3383562e2583edb16dab8b2b5e30')
    version('215.4', '2f1d40b865e65f0be05f62d092a193ca')
    version('215.3', 'd154a46c818350bfc3f0da3efd39c8f6')
    version('215.2', '4243b944cab04be0c5410e66db85f01c')
    version('215',   'b54886924bcf9bf7648437f4631dac20')

    patch('photos-215.5-update-configure.patch')

    def install(self, spec, prefix):
        cmsplatf=spec.architecture
        with working_dir(self.version.string):
            configure('--enable-static', '--disable-shared', '--lcgplatform=%s' % cmsplatf)
            make()
            du.copy_tree('lib', prefix.lib)
            du.copy_tree('include', prefix.include)
            for f in glob.glob(prefix.lib+'/archive/*.a'):
                shutil.move(f, prefix.lib+'/'+os.path.basename(f))
            shutil.rmtree(prefix.lib+'/archive')

    def url_for_version(self,version):
        url='http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/photos/photos-%s-src.tgz'%version
        return url

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'photos.xml'
        contents = str("""
<tool name="photos" version="${VER}">
  <lib name="photos"/>
  <client>
    <environment name="PHOTOS_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$PHOTOS_BASE/lib"/>
  </client>
  <use name="photos_headers"/>
  <use name="f77compiler"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)

        fname = 'photos_headers.xml'
        contents = str("""
<tool name="photos_headers" version="${VER}">
  <client>
    <environment name="PHOTOS_HEADERS_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$PHOTOS_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")

        write_scram_toolfile(contents, values, fname)

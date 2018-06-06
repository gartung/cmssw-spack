from spack import *
import glob
import distutils.dir_util as du
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile 


class Cascade(Package):


    homepage = "http://www.example.com"
    url      = "http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/cascade/cascade-2.2.04-src.tgz"

    version('2.2.04', '01986cfd390c41c6a3e066ff504aa1eb')

    depends_on('lhapdf')
    depends_on('pythia6')

    patch('cascade-2.2.04-drop-dcasrn.patch')

    def install(self, spec, prefix):
       with working_dir(self.version.string):
            configure('--prefix=%s' % prefix,
                      '--enable-static', '--disable-shared', 
                      '--with-pythia6=%s' % spec['pythia6'].prefix,
                      '--with-lhapdf=%s' % spec['lhapdf'].prefix,
                      'LIBS=-lstdc++ -lz','F77=gfortran -fPIC'
                      )
            make()
            make('install')


    @run_after('install')
    def make_merged_lib(self):
        with working_dir(self.prefix.lib):
            ar=which('ar')
            for file in glob.glob('*.a'):
                ar('-x',file)
            args=['rcs', 'libcascade_merged.a']
            for file in glob.glob('*.o'):
                args.append(file)
            ar(*args)
            for file in glob.glob('*.o'):
                os.remove(file)



    def url_for_version(self,version):
        url="http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/cascade/cascade-%s-src.tgz"%version
        return url

    @run_after('install')
    def write_scram_toolfiles(self):
        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix

        fname = 'cascade.xml'
        contents = str("""
<tool name="cascade" version="${VER}">
    <lib name="cascade_merged"/>
  <client>
    <environment name="CASCADE_BASE" default="${PFX}"/>
    <environment name="LIBDIR" default="$$CASCADE_BASE/lib"/>
  </client>
  <runtime name="CASCADE_PDFPATH" value="$$CASCADE_BASE/share"/>
  <use name="f77compiler"/>
  <use name="cascade_headers"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)

        fname = 'cascade_headers.xml'
        contents = str("""
<tool name="cascade_headers" version="${VER}">
  <client>
    <environment name="CASCADE_HEADERS_BASE" default="${PFX}"/>
    <environment name="INCLUDE" default="$$CASCADE_HEADERS_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname)


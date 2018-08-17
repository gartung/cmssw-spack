from spack import *
import glob
import distutils.dir_util as du
import sys,os


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

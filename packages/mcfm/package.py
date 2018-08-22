from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile
import glob

class Mcfm(Package):
    homepage = "http://www.example.com"
    url      = "http://www.example.com/example-1.2.3.tar.gz"

    version('6.3', git='https://github.com/cms-externals/MCFM', commit='d2e025ce8044976b95811b1a92e802f5e4eeb5ae')

    depends_on('root')

    def install(self, spec, prefix):
        mkdirp('obj')
        filter_file(r'MCFMHOME.*=.*', 'MCFMHOME = %s' % self.stage.source_path, 'makefile')
        filter_file(r'HERE.*=.*','HERE = %s/QCDLoop' % self.stage.source_path, 'QCDLoop/makefile')
        filter_file(r'HERE.*= .*','HERE = %s/QCDLoop/ff' % self.stage.source_path, 'QCDLoop/ff/makefile')
        filter_file(r'gfortran','gfortran -std=legacy', 'QCDLoop/ff/makefile')
        filter_file(r'gfortran','gfortran -std=legacy', 'QCDLoop/makefile')
        filter_file(r'gfortran','gfortran -std=legacy', 'makefile')
        filter_file(r'FFLAGS   = ','FFLAGS   =  -std=legacy ', 'makefile')
        filter_file(r'F90FLAGS = ','F90FLAGS = -std=legacy ', 'makefile')

        with working_dir(join_path(self.stage.source_path,'QCDLoop')):
            make('-j1', 'F77FLAGS=-std=legacy')

        with working_dir(self.stage.source_path):
            make('-j1', 'F77FLAGS=-std=legacy')
        os.remove('Bin/mcfm')
        mkdirp('lib')
        ar=which('ar')
        args=['cr','lib/libMCFM.a']
        for f in glob.glob('obj/*.o'):
            args.append(f)
        ar(*args)
        install_tree('lib',prefix.lib)
        install_tree('Bin',prefix.bin)

from spack import *
import distutils.dir_util as du
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Csctrackfinderemulation(Package):


    homepage = "http://www.example.com"
    url      = "http://www.example.com/example-1.2.3.tar.gz"

    version('1.2', git='https://github.com/cms-externals/CSCTrackFinderEmulation', branch='cms/CMSSW_8_1_X')


    def install(self, spec, prefix):
        make()
        make('install')
        du.copy_tree('installDir',prefix)

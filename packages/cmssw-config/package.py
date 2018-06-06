from spack import *

class CmsswConfig(Package):



    homepage = "http://www.example.com"
    url      = "http://www.example.com/example-1.2.3.tar.gz"


    version('V05-07-00', git='https://github.com/cms-sw/cmssw-config.git', tag='V05-07-00')


    def install(self, spec, prefix):

        install_tree(self.stage.source_path,prefix.bin)

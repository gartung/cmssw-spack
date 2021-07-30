from spack import *
from glob import glob
import sys,os

class FireworksGeometry(Package):
    url = "https://github.com/cms-data/Fireworks-Geometry/archive/V07-05-01.tar.gz"

    version('07-06-00', sha256='93312e7c60525c66c09c86fdc36db401c281b95ccb2d9195d735f84506f5868b')

    def install(self, spec, prefix):
        matches = []
        instpath = prefix.share+'/data/'
        mkdirp(instpath)
        for m in glob('*.root'):
            install(m, join_path(instpath, m))

    def url_for_version(self, version):
        """Handle CMSSW's version string."""
        return "https://github.com/cms-data/Fireworks-Geometry/archive/V%s.tar.gz" % version.dashed


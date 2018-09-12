from spack import *
from glob import glob
import sys,os

class FireworksGeometry(Package):
    url = "https://github.com/cms-data/Fireworks-Geometry/archive/V07-05-01.tar.gz"

    version('07.05.01', '9f40fdf89286392d1d39d5ed52981051')
    version('07.05.02', '0277dd37c0ff7664ea733445445efb6a')
    version('07.05.03', 'cea2d9a9c03cb95470552f7fd73d3537')
    version('07.05.04', 'ba4dd9a8eda665223e773c883cd367b2')


    def install(self, spec, prefix):
        matches = []
        instpath = prefix.share+'/data/'
        mkdirp(instpath)
        for m in glob('*.root'):
            install(m, join_path(instpath, m))

    def url_for_version(self, version):
        """Handle CMSSW's version string."""
        return "https://github.com/cms-data/Fireworks-Geometry/archive/V%s.tar.gz" % version.dashed


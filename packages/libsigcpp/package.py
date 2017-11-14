from spack import *

class Libsigcpp(Package):
    """Description"""

    homepage = "http://www.example.com"
    url      = "http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc630/external/sigcpp/2.6.2/libsigc++-2.6.2.tar.xz"

    version('2.6.2', 'd2f33ca0b4b012ef60669e3b3cebe956')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
        cp=which('cp')
        cp(prefix+'/lib/sigc++-2.0/include/sigc++config.h', prefix+'/include/sigc++-2.0/')

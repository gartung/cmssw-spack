from spack import *


class Gbl(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    url = "http://svnsrv.desy.de/public/GeneralBrokenLines/tags/V02-01-03/cpp"

    version('02-01-03', sha256='84e8328c4bde35d33e3a755cefbf00fcd285135c77f11ad331bbaed3a577ac12',
             url="http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc7_amd64_gcc810/external/gbl/V02-01-03/gbl-V02-01-03.tgz")

    # FIXME: Add dependencies if required.
    depends_on('eigen')

    def cmake_args(self):
        args = ['-DEIGEN3_INCLUDE_DIR=%s/include/eigen3'%self.spec['eigen'].prefix 
               ,'-DSUPPORT_ROOT=False']
        return args

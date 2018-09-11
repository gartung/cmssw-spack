from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile

class PyCython(PythonPackage):

    url = "http://cern.ch/service-spi/external/MCGenerators/distribution/cython/cython-0.22-src.tgz"

    version('0.28.3', '1aae6d6e9858888144cea147eb5e677830f45faaff3d305d77378c3cba55f526',
            url='http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc6_amd64_gcc700/external/py2-cython/0.28.3/source.tar.gz')

        

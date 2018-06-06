from spack import *
import platform
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Vecgeom(CMakePackage):
    """The vectorized geometry library for particle-detector simulation
    (toolkits)."""

    homepage = "https://gitlab.cern.ch/VecGeom/VecGeom"
 
    version('0.5.0', git='https://gitlab.cern.ch/VecGeom/VecGeom.git',
            tag='v00.05.00')
    version('0.3.rc', git='https://gitlab.cern.ch/VecGeom/VecGeom.git',
            tag='v0.3.rc')

    depends_on('cmake@3.5:', type='build')

    def cmake_args(self):
        options = [
            '-DBACKEND=Scalar',
            '-DGEANT4=OFF',
            '-DUSOLIDS=ON',
            '-DUSOLIDS_VECGEOM=ON',
            '-DROOT=OFF ',
            '-DNO_SPECIALIZATION=ON'
        ]

        arch = platform.machine()
        if arch == 'x86_64':
            options.append('-DVECGEOM_VECTOR=sse3')
        else:
            options.append('-DVECGEOM_VECTOR=' + arch)
        return options

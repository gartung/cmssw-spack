from spack import *
import glob
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile

class Openloops(Package):
    homepage = "http://www.example.com"
    url      = "https://github.com/cms-externals/openloops/archive/v1.1.1.tar.gz"

    version('1.3.1', git='https://github.com/cms-externals/openloops', branch='cms/v1.3.1')
    version('1.2.3', git='https://github.com/cms-externals/openloops', branch='cms/v1.2.3')
    version('1.1.1', '1b87db455871014afed01d2193d8758c')
    version('1.0.1', '4b6381c8bc1b62855d604b1c37ed5189')

    depends_on('python', type='build')
    depends_on('scons', type='build')

    patch('openloops-1.2.3-cpp-use-undef.patch')

    def patch(self):
        contents="""
[OpenLoops]
import_env = @all
fortran_compiler = gfortran
gfortran_f90_flags = -ffixed-line-length-0 -ffree-line-length-0 -O0
loop_optimisation = -O0
generic_optimisation = -O0
born_optimisation = -O0
"""
        filename='openloops.cfg'
        with open(filename, 'w') as f:
            f.write(contents)
            f.close()

    def install(self, spec, prefix):
        builder = Executable('./openloops')
        builder('update', '--processes', 'generator=0')
        mkdirp(prefix.lib)
        mkdirp(join_path(prefix, 'proclib'))
        for f in glob.glob('lib/*.so'):
            install(f, join_path(prefix, f))
        for f in glob.glob('proclib/*.so'):
            install(f, join_path(prefix, f))
        for f in glob.glob('proclib/*.info'):
            install(f, join_path(prefix, f))


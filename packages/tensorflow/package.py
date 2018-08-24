from spack import *
from llnl.util.filesystem import *
import os
from glob import glob
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Tensorflow(Package):
    """
    TensorFlow is an open source software library for numerical computation using data flow graphs
    """

    homepage = "https://www.tensorflow.org/"

    version('1.3.0', git='https://github.com/tensorflow/tensorflow.git', tag='v1.3.0')

    depends_on('bazel', type='build')
    depends_on('swig', type='build')
    depends_on('python', type='build')

    patch('tensorflow-workspace.patch')

    def install(self, spec, prefix):
        configure()
        bazel=which('bazel')
        bazel('fetch', 'tensorflow:libtensorflow_cc.so')
        for f in find('./dud', 'protobuf.bzl'):
            print f
            filter_file('mnemonic="ProtoCompile",','mnemonic="ProtoCompile", env=ctx.configuration.default_shell_env, ', f)
        for f in find('./dud','*/external/protobuf/BUILD'):
            print f
            filter_file('"-lpthread", "-lm"','"-lpthread", "-lm", "-lrt"', f)
        bazel('build', '-s', '--verbose_failures', '-c', 'opt', '--cxxopt=%s' % env['CXX_OPT_FLAGS'],
              '//tensorflow/tools/lib_package:libtensorflow')
        bazel('shutdown') 
        mkdirp(prefix.lib)
        for f in find('bazel-bin/tensorflow/','libtensorflow_cc.so'):
            install(f, prefix.lib)
        depdl=Executable('tensorflow/contrib/makefile/download_dependencies.sh')
        depdl()
        mkdirp(prefix.include)
        for f in find('tensorflow', '*.h'):
            mkdirp('%s/%s' % (prefix.include, os.path.dirname(f)))
            install(f, '%s/%s' % (prefix.include, os.path.dirname(f)))
        for g in find('third_party', '*.h'):
            if not str(g).find('contrib'):
                mkdirp('%s/%s' % (prefix.include, os.path.dirname(g)))
                install(g, '%s/%s' % (prefix.include, os.path.dirname(g)))
        for h in find('third_party/eigen3', '*'):
            if not str(h).find('contrib'):
                mkdirp('%s/%s' % (prefix.include, os.path.dirname(h)))
                install(h, '%s/%s' % (prefix.include, os.path.dirname(h)))
        with working_dir('./tensorflow/contrib/makefile/downloads'):
            for i in find('gemmlowp','*.h'):
                mkdirp('%s/%s' % (prefix.include, os.path.dirname(i)))
                install(i, '%s/%s' % (prefix.include, os.path.dirname(i)))
            for j in find('googletest','*.h'):
                mkdirp('%s/%s' % (prefix.include, os.path.dirname(j)))
                install(i, '%s/%s' % (prefix.include, os.path.dirname(j)))
            for k in find('re2','*.h'):
                mkdirp('%s/%s' % (prefix.include, os.path.dirname(k)))
                install(k, '%s/%s' % (prefix.include, os.path.dirname(k)))
            for l in find('eigen/Eigen','*'):
                mkdirp('%s/%s' % (prefix.include, os.path.dirname(l)))
                install(l, '%s/%s' % (prefix.include, os.path.dirname(l)))
            for m in find('eigen/unsupported','*'):
                mkdirp('%s/%s' % (prefix.include, os.path.dirname(m)))
                install(m, '%s/%s' % (prefix.include, os.path.dirname(m)))
            if os.path.exists('eigen/signature_of_eigen3_matrix_library'):
                install('eigen/signature_of_eigen3_matrix_library', '%s/eigen' % prefix.include)
        
#    def setup_environment(self, spack_env, run_env):
#        spack_env.set('PYTHON_BIN_PATH', '%s/python' % self.spec['python'].prefix.bin )
#        spack_env.set('TF_NEED_JEMALLOC','0')
#        spack_env.set('TF_NEED_HDFS', '0')
#        spack_env.set('CC_OPT_FLAGS', '-march=core2')
#        spack_env.set('CXX_OPT_FLAGS', '-std=c++11')
#        spack_env.set('TF_NEED_GCP', '0')
#        spack_env.set('TF_ENABLE_XLA', '0')
#        spack_env.set('TF_NEED_OPENCL', '0')
#        spack_env.set('TF_NEED_CUDA', '0')
#        spack_env.set('TF_NEED_VERBS', '0')
#        spack_env.set('TF_NEED_MKL', '0')
#        spack_env.set('TF_NEED_MPI', '0')
#        spack_env.set('USE_DEFAULT_PYTHON_LIB_PATH', '1')
#        spack_env.set('TEST_TMPDIR', './dud')
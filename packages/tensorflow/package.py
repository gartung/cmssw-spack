##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
from llnl.util.filesystem import *
import os


class Tensorflow(Package):
    """
    TensorFlow is an open source software library for numerical computation using data flow graphs
    """

    homepage = "https://www.tensorflow.org/"

    version('1.6.0', git='https://github.com/cms-externals/tensorflow.git',
            commit='6eea62c87173ad98c71f10ff2f796f6654f5b604')

    depends_on('bazel@0.11.0', type='build')
    depends_on('swig', type='build')
    depends_on('python', type='build')
    depends_on('py-numpy')
    depends_on('py-wheel')
    depends_on('eigen')
    depends_on('protobuf')

    patch('tensorflow-1.6.0-rename-runtime.patch')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('TF_NEED_S3', '0')
        spack_env.set('TF_NEED_GCP', '0')
        spack_env.set('TF_NEED_HDFS', '0')
        spack_env.set('TF_NEED_JEMALLOC','0')
        spack_env.set('TF_NEED_KAFKA', '0')
        spack_env.set('TF_NEED_OPENCL_SYCL', '0')
        spack_env.set('TF_NEED_COMPUTECPP', '0')
        spack_env.set('TF_NEED_OPENCL', '0')
        spack_env.set('TF_CUDA_CLANG', '0')
        spack_env.set('TF_NEED_TENSORRT', '0')
        spack_env.set('TF_ENABLE_XLA', '0')
        spack_env.set('TF_NEED_GDR', '0')
        spack_env.set('TF_NEED_VERBS', '0')
        spack_env.set('TF_NEED_CUDA', '0')
        spack_env.set('TF_NEED_MKL', '0')
        spack_env.set('TF_NEED_MPI', '0')
        spack_env.set('TF_SET_ANDROID_WORKSPACE', '0')
        spack_env.set('CC_OPT_FLAGS', '-march=core2')
        spack_env.set('CXX_OPT_FLAGS', '-std=c++11')
        spack_env.set('USE_DEFAULT_PYTHON_LIB_PATH', '1')
        spack_env.set('PYTHON_BIN_PATH', '%s/python' % self.spec['python'].prefix.bin )


    def relinstall(f, target):
        if os.path.isfile(f) and not os.path.islink(f):
            rp=os.path.relpath(os.path.dirname(f))
            mkdirp('%s/%s' % (target,rp))
            install(f, '%s/%s' % (target, rp))


    def install(self, spec, prefix):
        base='--output_base=%s/base'%self.stage.path
        user_root='--output_user_root=%s/user_root'%self.stage.path
        filename=join_path(self.stage.path,'tensorflow','.bazelrc')
        with open(filename,'w') as f:
            f.write('startup '+base+' '+user_root+'\n')
        configure()
        for f in ['tensorflow/workspace.bzl','tensorflow/contrib/makefile/download_dependencies.sh']:
            filter_file('@EIGEN_SOURCE@', env['EIGEN_SOURCE'],f)
            filter_file('@EIGEN_STRIP_PREFIX@', env['EIGEN_STRIP_PREFIX'],f)
            filter_file('@PROTOBUF_SOURCE@',  env['PROTOBUF_SOURCE'],f)
            filter_file('@PROTOBUF_STRIP_PREFIX@', env['PROTOBUF_STRIP_PREFIX'], f)
        bazel=which('bazel')

        bazel('fetch', 'tensorflow:libtensorflow_cc.so')

        for f in find(self.stage.path,'base/external/org_tensorflow/tensorflow/tensorflow.bzl'):
            filter_file('executable=ctx.executable._swig,','env=ctx.configuration.default_shell_env, executable=ctx.executable._swig,',f)
        for f in find(self.stage.path, 'base/external/protobuf_archive/protobuf.bzl'):
            filter_file('mnemonic="ProtoCompile",','env=ctx.configuration.default_shell_env, mnemonic="ProtoCompile",', f)
        for f in find(self.stage.path,'base/external/protobuf/BUILD'):
            filter_file('"-lpthread", "-lm"','"-lpthread", "-lm", "-lrt"', f)

        bazel('build', '-s', '--verbose_failures', '-c', 'opt', '--cxxopt=%s' % env['CXX_OPT_FLAGS'],
              '//tensorflow:libtensorflow_cc.so')
        bazel('build', '-s', '--verbose_failures', '-c', 'opt', '--cxxopt=%s' % env['CXX_OPT_FLAGS'],
              '//tensorflow/tools/pip_package:build_pip_package')
        bazel('build', '-s', '--verbose_failures', '-c', 'opt', '--cxxopt=%s' % env['CXX_OPT_FLAGS'],
              '//tensorflow/tools/lib_package:libtensorflow')
        bazel('build', '-s', '--verbose_failures', '-c', 'opt', '--cxxopt=%s' % env['CXX_OPT_FLAGS'],
              '//tensorflow/python/tools:tools_pip')
        bazel('build', '-s', '--verbose_failures', '-c', 'opt', '--cxxopt=%s' % env['CXX_OPT_FLAGS'],
              '//tensorflow/tools/graph_transforms:transform_graph')
        bazel('build', '-s', '--verbose_failures', '-c', 'opt', '--cxxopt=%s' % env['CXX_OPT_FLAGS'],
              '//tensorflow/compiler/aot:tf_aot_runtime')
        bazel('build', '-s', '--verbose_failures', '-c', 'opt', '--cxxopt=%s' % env['CXX_OPT_FLAGS'],
              '//tensorflow/compiler/tf2xla:xla_compiled_cpu_function')
        bazel('build', '-s', '--verbose_failures', '-c', 'opt', '--cxxopt=%s' % env['CXX_OPT_FLAGS'],
              '//tensorflow/compiler/aot:tfcompile')

        bazel('shutdown')

        build_pip_package=Executable('bazel-bin/tensorflow/tools/pip_package/build_pip_package')
        build_pip_package('%s' % self.prefix)

      
        libdir='%s/tensorflow_cc/lib' % os.getcwd()
        bindir='%s/tensorflow_cc/bin' % os.getcwd()
        incdir='%s/tensorflow_cc/include' % os.getcwd()

        for f in find('bazel-bin/tensorflow/','libtensorflow_cc.so'):
            relinstall(os.path.basename(f), libdir)
        for f in find('bazel-bin/tensorflow/','libtensorflow_framework.so'):
            relinstall(os.path.basename(f), libdir)
        for f in find('bazel-bin/tensorflow/compiler/aot','libtf_aot_runtime.so'):
            relinstall(os.path.basename(f), libdir)
        for f in find('bazel-bin/tensorflow/compiler/tf2xla', 'libxla_compiled_cpu_function.so'):
            relinstall(os.path.basename(f), libdir)
        for f in find('bazel-bin/tensorflow/compiler/aot','tfcompile'):
            relinstall(os.path.basebane(f), bindir)

        depdl=Executable('tensorflow/contrib/makefile/download_dependencies.sh')
        depdl()

        for d in ('tensorflow','third_party', 'third_party/eigen3'):
            for f in find( d, '*.h'):
                relinstall(f, incdir)

        with working_dir('./bazel-genfiles'):
            for f in find('tensorflow','*.h'):
                if str(f).find('contrib') == -1:
                    relinstall(f, incdir)

        with working_dir('./tensorflow/contrib/makefile/downloads'):
            for d in ('gemmlowp', 'googletest', 're2', 'eigen/Eigen', 'eigen/unsupported','nsync/public'):
                for f in find( d,'*.h'):
                    relinstall(f, incdir)
            f='eigen/signature_of_eigen3_matrix_library'
            if os.path.exists(f):
                relinstall(f, incdir)
        tar='bazel-bin/tensorflow/tools/lib_package/libtensorflow.tar.gz'
        if os.path.exists(tar):
            install(tar, prefix.share)
        install_tree(incdir, prefix.include)
        install_tree(libdir, prefix.lib)
        install_tree(bindir, prefix.bin)

from spack import *
import os
import glob
import fnmatch

class CudaBin(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "http://developer.nvidia.com"
    url      = "https://developer.nvidia.com/compute/cuda/9.2/Prod2/local_installers/cuda_9.2.148_396.37_linux"

    version('9.2.148_396.37', url="https://developer.nvidia.com/compute/cuda/9.2/Prod2/local_installers/cuda_9.2.148_396.37_linux",
            sha256='f5454ec2cfdf6e02979ed2b1ebc18480d5dded2ef2279e9ce68a505056da8611',expand=False)

    resource(name='cuda-patch', url='https://developer.nvidia.com/compute/cuda/9.2/Prod2/patches/1/cuda_9.2.148.1_linux',
           sha256='9c8a2af575af998dfa2f9050c78b14d92dc8fd65946ee20236b32afd3da1a6cf',expand=False, placement='cuda-patch') 

    def install(self, spec, prefix):
        ver='9.2.148'
        dver='396.37'
        sh=which('sh')
        mkdirp('tmp')
        sh('cuda_%s_%s_linux' % (ver,dver), '--silent', '--tmpdir','%s/tmp' % self.stage.path, '--extract', '%s' % self.stage.path)
        rf=glob.glob('cuda-linux.%s-*.run'%ver)
        sh(rf[0], '-noprompt', '-nosymlink', 
           '-tmpdir', '%s/tmp' % self.stage.path, '-prefix', '%s' % prefix)
        sh('cuda-patch/cuda_%s.1_linux' % ver, '--silent', '--accept-eula', 
           '--tmpdir', '%s/tmp' % self.stage.path, '--installdir',  '%s' % prefix)
        with working_dir(prefix):
            os.remove('lib64/libcublas.so.%s'%ver)
            os.remove('lib64/libnvblas.so.%s'%ver)
            os.remove('lib64/libcuinj64.so.%s'%ver)
            os.remove('extras/CUPTI/lib64/libcupti.so.%s'%ver)
# package only runtime and device static libraries
            keep=('lib64/libcublas_device.a', 'lib64/libcudadevrt.a', 'lib64/libcudart_static.a')
            for f in glob.glob('lib64/lib*.a'):
                if not f in keep:
                    print(f)
                    os.remove(f) 
# do not package dynamic libraries for which we have stubs
            for f in glob.glob('lib64/libcublas.so*'):
                os.remove(f)
            for f in glob.glob('lib64/libcufft.so*'):
                os.remove(f)
            for f in glob.glob('lib64/libcufftw.so*'):
                os.remove(f)
            for f in glob.glob('lib64/libcurand.so*'):
                os.remove(f)
            for f in glob.glob('lib64/libcusolver.so*'):
                os.remove(f)
            for f in glob.glob('lib64/libcusparse.so*'):
                os.remove(f)
            for f in glob.glob('lib64/libnpp*.so*'):
                os.remove(f)
            for f in glob.glob('lib64/libnvgraph.so*'):
                os.remove(f)


# package the includes
        os.remove('%s/include/sobol_direction_vectors.h'%prefix)
# leave out nsight and nvvp
        os.remove('%s/bin/nsight'%prefix)
        os.remove('%s/bin/nvvp'%prefix)
        os.remove('%s/bin/computeprof'%prefix)
# package the cuda-gdb support files, and rename the binary to use it via a wrapper
        os.rename('%s/bin/cuda-gdb'%prefix, '%s/bin/cuda-gdb.real'%prefix)
        sh('NVIDIA-Linux-x86_64-%s.run'%dver, '--accept-license', '--extract-only', 
           '--tmpdir', '%s/tmp' % self.stage.path, 
           '--target', '%s/drivers' % prefix)

        with working_dir('%s/drivers' % prefix):
            os.symlink('libcuda.so.%s'%dver, 'libcuda.so.1')
            os.symlink('libnvidia-ptxjitcompiler.so.%s'%dver, 'libnvidia-ptxjitcompiler.so.1')

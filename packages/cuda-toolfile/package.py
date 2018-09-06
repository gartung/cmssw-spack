from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class CudaToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../../common/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('cuda-bin')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['cuda-bin'].version
        values['PFX'] = self.spec['cuda-bin'].prefix
        fname = 'cuda-stubs.xml'
        contents = str("""
<tool name="cuda-stubs" version="$VER">
  <info url="https://docs.nvidia.com/cuda/index.html"/>
  <lib name="cuda"/>
  <client>
    <environment name="CUDA_STUBS_BASE" default="$PFX"/>
    <environment name="LIBDIR"          default="$$CUDA_STUBS_BASE/lib64/stubs"/>
    <environment name="INCLUDE"         default="$$CUDA_STUBS_BASE/include"/>
  </client>
  <flags SKIP_TOOL_SYMLINKS="1"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

        fname = 'cuda.xml'
        contents = str("""
<tool name="cuda" version="$VER">
  <info url="https://docs.nvidia.com/cuda/index.html"/>
  <use name="cuda-stubs"/>
  <lib name="cudart"/>
  <lib name="cudadevrt"/>
  <lib name="nvToolsExt"/>
  <client>
    <environment name="CUDA_BASE" default="$PFX"/>
    <environment name="NVCC"      default="$$CUDA_BASE/bin/nvcc"/>
    <environment name="BINDIR"    default="$$CUDA_BASE/bin"/>
    <environment name="LIBDIR"    default="$$CUDA_BASE/lib64"/>
    <environment name="INCLUDE"   default="$$CUDA_BASE/include"/>
  </client>
  <flags CUDA_FLAGS="-gencode arch=compute_35,code=sm_35"/>
  <flags CUDA_FLAGS="-gencode arch=compute_50,code=sm_50"/>
  <flags CUDA_FLAGS="-gencode arch=compute_61,code=sm_61"/>
  <flags CUDA_FLAGS="-O3 -std=c++14 --expt-relaxed-constexpr --expt-extended-lambda"/>
  <flags CUDA_HOST_REM_CXXFLAGS="-std=%"/>
  <flags CUDA_HOST_REM_CXXFLAGS="%potentially-evaluated-expression"/>
  <flags CUDA_HOST_CXXFLAGS="-std=c++14"/>
  <lib name="cudadevrt" type="cuda"/>
  <runtime name="PATH" value="$$CUDA_BASE/bin" type="path"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)


        fname='cuda-cublas.xml'
        contents = str("""
<tool name="cuda-cublas" version="$VER">
  <info url="https://docs.nvidia.com/cuda/cublas/index.html"/>
  <use name="cuda"/>
  <lib name="cublas"/>
  <lib name="cublas_device"/>
  <lib name="cublas_device" type="cuda"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

        fname='cuda-cufft.xml'
        contents = str("""
<tool name="cuda-cufft" version="$VER">
  <info url="https://docs.nvidia.com/cuda/cufft/index.html"/>
  <use name="cuda"/>
  <lib name="cufft"/>
  <lib name="cufftw"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

        fname='cuda-curand.xml'
        contents = str("""
<tool name="cuda-curand" version="$VER">
  <info url="https://docs.nvidia.com/cuda/curand/index.html"/>
  <use name="cuda"/>
  <lib name="curand"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

        fname='cuda-cusolver.xml'
        contents = str("""
<tool name="cuda-cusolver" version="$VER">
  <info url="https://docs.nvidia.com/cuda/cusolver/index.html"/>
  <use name="cuda"/>
  <lib name="cusolver"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

        fname='cuda-cusparse.xml'
        contents = str("""
<tool name="cuda-cusparse" version="$VER">
  <info url="https://docs.nvidia.com/cuda/cusparse/index.html"/>
  <use name="cuda"/>
  <lib name="cusparse"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

        fname='cuda-npp.xml'
        contents = str("""
<tool name="cuda-npp" version="$VER">
  <info url="https://docs.nvidia.com/cuda/npp/index.html"/>
  <use name="cuda"/>
  <lib name="nppial"/>
  <lib name="nppicc"/>
  <lib name="nppicom"/>
  <lib name="nppidei"/>
  <lib name="nppif"/>
  <lib name="nppig"/>
  <lib name="nppim"/>
  <lib name="nppist"/>
  <lib name="nppisu"/>
  <lib name="nppitc"/>
  <lib name="npps"/>
  <lib name="nppc"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

        fname='cuda-nvgraph.xml'
        contents = str("""
<tool name="cuda-nvgraph" version="$VER">
  <info url="https://docs.nvidia.com/cuda/nvgraph/index.html"/>
  <use name="cuda"/>
  <lib name="nvgraph"/>
</tool>
""")

        fname='cuda-nvml.xml'
        contents = str("""
<tool name="cuda-nvml" version="$VER">
  <info url="https://docs.nvidia.com/deploy/nvml-api/index.html"/>
  <use name="cuda"/>
  <lib name="nvidia-ml"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

        fname='cuda-nvrtc.xml'
        contents = str("""
<tool name="cuda-nvrtc" version="$VER">
  <info url="https://docs.nvidia.com/cuda/nvrtc/index.html"/>
  <use name="cuda"/>
  <lib name="nvrtc"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

        fname='nvidia-drivers.xml'
        contents = str("""
<tool name="nvidia-drivers" version="$VER">
  <info url="https://docs.nvidia.com/cuda/index.html"/>
  <client>
    <environment name="NVIDIA_DRIVERS_BASE" default="$PFX"/>
    <environment name="LIBDIR"              default="$$NVIDIA_DRIVERS_BASE/drivers"/>
  </client>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)

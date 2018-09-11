from spack import *
import sys
import re
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class Root(CMakePackage):
    """ROOT is a data analysis framework."""
    homepage = "https://root.cern.ch"
    url = "https://root.cern.ch/download/root_v6.07.02.source.tar.gz"
    

    version('6.12.07', git='https://github.com/cms-sw/root.git', commit='8ea59a196e04c88776a05f9d20fac287f05224f6')


    depends_on('cmake@3.4.3:', type='build')
    depends_on('pkg-config',   type='build')
    depends_on("pcre")
    depends_on("fftw")
    depends_on("python")
    depends_on("gsl")
    depends_on('libice')
    depends_on('libpng')
    depends_on('libsm')
    depends_on('libx11')
    depends_on('libxext')
    depends_on('libxft')
    depends_on('libxpm')
    depends_on("libxml2")
    depends_on("libjpeg-turbo")
    depends_on("libpng")
    depends_on("libtiff")
    depends_on("giflib")
    depends_on("xz")
    depends_on('zlib')
    depends_on("openssl")
    depends_on("xrootd")
    depends_on("freetype")
    if sys.platform == 'linux2':
        depends_on("dcap") 
    depends_on("davix", type='run')
    depends_on("openblas")
    depends_on("intel-tbb")

    def cmake_args(self):
        pyvers = str(self.spec['python'].version).split('.')
        pyver = pyvers[0] + '.' + pyvers[1]
        options = [  '-Droot7=ON'
                    ,'-Dfail-on-missing=ON'
                    ,'-Dgnuinstall=OFF'
                    ,'-Droofit=ON'
                    ,'-Dvdt=OFF'
                    ,'-Dhdfs=OFF'
                    ,'-Dqt=OFF'
                    ,'-Dqtgsi=OFF'
                    ,'-Dpgsql=OFF'
                    ,'-Dsqlite=OFF'
                    ,'-Dmysql=OFF'
                    ,'-Doracle=OFF'
                    ,'-Dldap=OFF'
                    ,'-Dkrb5=OFF'
                    ,'-Dftgl=OFF'
                    ,'-Dfftw3=ON'
                    ,'-Dtbb=ON'
                    ,'-Dimt=ON'
                    ,'-DFFTW_INCLUDE_DIR=%s' %
                      self.spec['fftw'].prefix.include
                    ,'-DFFTW_LIBRARY=%s/libfftw3.%s'%
                     (self.spec['fftw'].prefix.lib, dso_suffix)
                    ,'-Dminuit2=ON'
                    ,'-Dmathmore=ON'
                    ,'-Dexplicitlink=ON'
                    ,'-Dtable=ON'
                    ,'-Dbuiltin_tbb=OFF'
                    ,'-Dbuiltin_pcre=OFF'
                    ,'-Dbuiltin_freetype=OFF'
                    ,'-Dbuiltin_zlib=OFF'
                    ,'-Dbuiltin_lzma=OFF'
                    ,'-Dbuiltin_gsl=OFF'
                    ,'-DGSL_CONFIG_EXECUTABLE=%s/gsl-config' %
                      self.spec['gsl'].prefix.bin
                    ,'-Dcxx17=ON'
                    ,'-Dssl=ON'
                    ,'-DOPENSSL_ROOT_DIR=%s' %
                      self.spec['openssl'].prefix
                    ,'-DOPENSSL_INCLUDE_DIR=%s' %
                      self.spec['openssl'].prefix.include
                    ,'-Dpython=ON'
                    ,'-Dxrootd=ON'
                    ,'-Dbuiltin_xrootd=OFF'
                    ,'-DXROOTD_INCLUDE_DIR=%s/xrootd' %
                      self.spec['xrootd'].prefix.include
                    ,'-DXROOTD_ROOT_DIR=%s' %
                      self.spec['xrootd'].prefix
                    ,'-DCMAKE_C_FLAGS=-D__ROOFIT_NOBANNER'
                    ,'-Dgviz=OFF'
                    ,'-Dbonjour=OFF'
                    ,'-Dodbc=OFF'
                    ,'-Dpythia6=OFF'
                    ,'-Dpythia8=OFF'
                    ,'-Dfitsio=OFF'
                    ,'-Dgfal=OFF'
                    ,'-Dchirp=OFF'
                    ,'-Dsrp=OFF'
                    ,'-Ddavix=ON'
                    ,'-DDAVIX_DIR=%s' %
                      self.spec['davix'].prefix
                    ,'-Dglite=OFF'
                    ,'-Dsapdb=OFF'
                    ,'-Dalien=OFF'
                    ,'-Dmonalisa=OFF'
                    ,'-DLIBLZMA_INCLUDE_DIR=%s' %
                      self.spec['xz'].prefix.include
                    ,'-DLIBLZMA_LIBRARY=%s/liblzma.%s' %
                     (self.spec['xz'].prefix.lib, dso_suffix)
                    ,'-DZLIB_ROOT=%s' %
                      self.spec['zlib'].prefix
                    ,'-DZLIB_INCLUDE_DIR=%s' %
                      self.spec['zlib'].prefix.include
                    ,'-DLIBXML2_INCLUDE_DIR=%s/libxml2' %
                      self.spec['libxml2'].prefix.include
                    ,'-DLIBXML2_LIBRARY=%s/libxml2.%s' %
                     (self.spec['libxml2'].prefix.lib, dso_suffix)
                    ,'-DPCRE_CONFIG_EXECUTABLE=%s/bin/pcre-config' %
                      self.spec['pcre'].prefix
                    ,'-DPCRE_INCLUDE_DIR=%s' %
                      self.spec['pcre'].prefix.include
                    ,'-DPCRE_PCRE_LIBRARY=%s/libpcre.%s' %
                     (self.spec['pcre'].prefix.lib, dso_suffix)
                    ,'-DPCRE_PCREPOSIX_LIBRARY=%s/libpcreposix.%s' %
                     (self.spec['pcre'].prefix.lib, dso_suffix)
                    ,'-DPYTHON_EXECUTABLE=%s/python' %
                     (self.spec['python'].prefix.bin)
                    ,'-DPYTHON_INCLUDE=%s' %
                     (self.spec['python'].prefix.include)
                    ,'-DPYTHON_LIBRARY=%s/libpython2.7.%s' %
                     (self.spec['python'].prefix.lib, dso_suffix)
                   ]

        if sys.platform == 'linux2':
            linux_options = [
                     '-Drfio=OFF'
                    ,'-Dcastor=OFF'
                    ,'-Ddcache=ON'
                    ,'-DDCAP_INCLUDE_DIR=%s' %
                      self.spec['dcap'].prefix.include
                    ,'-DDCAP_DIR=%s' %
                      self.spec['dcap'].prefix
                    ,'-DJPEG_INCLUDE_DIR=%s' %
                      self.spec['libjpeg-turbo'].prefix.include
                    ,'-DJPEG_LIBRARY=%s/libjpeg.%s' %
                     (self.spec['libjpeg-turbo'].prefix.lib64, dso_suffix)
                    ,'-DPNG_INCLUDE_DIRS=%s' %
                      self.spec['libpng'].prefix.include
                    ,'-DPNG_LIBRARY=%s/libpng.%s' %
                     (self.spec['libpng'].prefix.lib, dso_suffix)
                    ,'-Dastiff=ON'
                    ,'-DTIFF_INCLUDE_DIR=%s' %
                      self.spec['libtiff'].prefix.include
                    ,'-DTIFF_LIBRARY=%s/libtiff.%s' %
                     (self.spec['libtiff'].prefix.lib, dso_suffix)
            ]
            options.extend(linux_options)

        if sys.platform == 'darwin':
            darwin_options = [
                '-Dx11=off',
                '-Dcocoa=on',
                '-Dbonjour=on',
                '-Dcastor=OFF',
                '-Drfio=OFF',
                '-Ddcache=OFF']
            options.extend(darwin_options)

        return options


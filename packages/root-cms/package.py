from spack import *
import sys
import re
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../common'))
from scrampackage import write_scram_toolfile


class RootCms(CMakePackage):
    """ROOT is a data analysis framework."""
    homepage = "https://root.cern.ch"
    url = "https://root.cern.ch/download/root_v6.07.02.source.tar.gz"
    
    version('6.10.09',
             '1bffe3ef37558d5773ab596758037ffa',
             url='http://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc7_amd64_gcc700/lcg/root/6.10.09-omkpbe3/root-6.10.09-287883fd1b96f3a53c80032651656565c3a04901.tgz')

    patch('root_new_cxx17.patch')

    depends_on('cmake@3.4.3:', type='build')
    depends_on('pkg-config',   type='build')
    depends_on("pcre")
    depends_on("fftw")
    depends_on("python")
    depends_on("gsl")
    depends_on("libxml2+python")
    depends_on("libjpeg-turbo")
    depends_on("libpng")
    depends_on("libtiff")
    depends_on("giflib")
    depends_on("xz")
    depends_on('zlib')
    depends_on("openssl")
    depends_on("xrootd")
    depends_on("freetype")
    depends_on("dcap")
    depends_on("davix")
    depends_on("openblas")
    depends_on("tbb")

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
                    ,'-DLIBXML2_LIBRARIES=%s/libxml2.%s' %
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
                     (self.spec['libjpeg-turbo'].prefix.lib, dso_suffix)
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

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('PATH', self.prefix.bin)
        run_env.set('ROOTSYS', self.prefix)
        run_env.set('ROOT_VERSION', 'v6')
        run_env.prepend_path('PYTHONPATH', self.prefix.lib)
        run_env.set('ROOT_TTREECACHE_SIZE', '0')
        run_env.set('ROOT_TTREECACHE_PREFILL', '0')
        spack_env.set('ROOTSYS', self.prefix)
        spack_env.set('PYTHONV','2.7')
        spack_env.append_flags('CFLAGS', '-D__ROOFIT_NOBANNER')
        spack_env.append_flags('CXXFLAGS', '-D__ROOFIT_NOBANNER')
        for d in self.spec.traverse(root=False, deptype=('link')):
            spack_env.append_path('ROOT_INCLUDE_PATH',str(self.spec[d.name].prefix.include))
            run_env.append_path('ROOT_INCLUDE_PATH',str(self.spec[d.name].prefix.include))

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('ROOTSYS', self.prefix)
        spack_env.set('ROOT_VERSION', 'v6')
        spack_env.prepend_path('PYTHONPATH', self.prefix.lib)
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.set('ROOTSYS', self.prefix)
        run_env.set('ROOT_VERSION', 'v6')
        run_env.prepend_path('PYTHONPATH', self.prefix.lib)
        run_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        for d in self.spec.traverse(root=False, deptype=('link')):
            spack_env.append_path('ROOT_INCLUDE_PATH',str(self.spec[d.name].prefix.include))
            run_env.append_path('ROOT_INCLUDE_PATH',str(self.spec[d.name].prefix.include))
        run_env.set('ROOT_TTREECACHE_SIZE', '0')
        run_env.set('ROOT_TTREECACHE_PREFILL', '0')

    def url_for_version(self, version):
        """Handle ROOT's unusual version string."""
        return "https://root.cern.ch/download/root_v%s.source.tar.gz" % version

    @run_after('install')
    def write_scram_toolfiles(self):
        gcc = which(spack_f77)
        gcc_prefix = re.sub('/bin/.*$', '', self.compiler.f77)
        gcc_machine = gcc('-dumpmachine', output=str)
        gcc_ver = gcc('-dumpversion', output=str)

        values = {}
        values['VER'] = self.spec.version
        values['PFX'] = self.spec.prefix
        values['GCC_VER'] = gcc_ver.rstrip()
        values['GCC_PREFIX'] = gcc_prefix
        values['GCC_MACHINE'] = gcc_machine.rstrip()

        fname = 'root_interface.xml'
        contents = str("""<tool name="root_interface" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <client>
    <environment name="ROOT_INTERFACE_BASE"     default="$PFX"/>
    <environment name="INCLUDE"                 default="$PFX/include"/>
    <environment name="LIBDIR"                  default="$PFX/lib"/>
  </client>
  <runtime name="PATH"                          value="$PFX/bin" type="path"/>
  <runtime name="PYTHONPATH"                    value="$PFX/lib" type="path"/>
  <runtime name="ROOTSYS"                       value="$PFX/"/>
  <runtime name="ROOT_TTREECACHE_SIZE"          value="0"/>
  <runtime name="ROOT_TTREECACHE_PREFILL"       value="0"/>
  <runtime name="ROOT_INCLUDE_PATH"             value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)

        fname = 'root_cxxdefaults.xml'
        contents = str("""<tool name="root_cxxdefaults" version="$VER">
  <runtime name="ROOT_GCC_TOOLCHAIN" value="$GCC_PREFIX" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$GCC_PREFIX/include/c++/$GCC_VER" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$GCC_PREFIX/include/c++/$GCC_VER/$GCC_MACHINE" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$GCC_PREFIX/include/c++/$GCC_VER/backward" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="/usr/local/include" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="/usr/include" type="path"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)

# rootcling toolfile
        fname = 'rootcling.xml'
        contents = str("""<tool name="rootcling" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Core"/>
  <client>
    <environment name="ROOTCLING_BASE" default="$PFX"/>
    <environment name="INCLUDE"        default="$PFX/include"/>
  </client>
  <use name="root_interface"/>
  <use name="sockets"/>
  <use name="pcre"/>
  <use name="zlib"/>
  <use name="xz"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)

# rootrint toolfile
        fname = 'rootrint.xml'
        contents = str("""<tool name="rootrint" version="$VER'">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Rint"/>
  <use name="rootcling"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)

# rootsmatrix toolfile
        fname = 'rootsmatrix.xml'
        contents = str("""<tool name="rootsmatrix" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Smatrix"/>
  <use name="rootcling"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rootrio toolfile
        fname = 'rootrio.xml'
        contents = str("""<tool name="rootrio" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RIO"/>
  <use name="rootcling"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rootthread toolfile
        fname = 'rootthread.xml'
        contents = str("""<tool name="rootthread" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Thread"/>
  <use name="rootrio"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rootxmlio toolfile
        fname = 'rootxmlio.xml'
        contents = str("""<tool name="rootxmlio" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="XMLIO"/>
  <use name="rootrio"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rootmathcore toolfile
        fname = 'rootmathcore.xml'
        contents = str("""<tool name="rootmathcore" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="MathCore"/>
  <use name="rootcling"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rootcore toolfile
        fname = 'rootcore.xml'
        contents = str("""<tool name="rootcore" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Tree"/>
  <lib name="Net"/>
  <use name="rootmathcore"/>
  <use name="rootthread"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# roothistmatrix toolfile
        fname = 'roothistmatrix.xml'
        contents = str("""<tool name="roothistmatrix" version="$VER"> 
  <info url="http://root.cern.ch/root/"/>
  <lib name="Hist"/>
  <lib name="Matrix"/>
  <use name="rootcore"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rootspectrum toolfile
        fname = 'rootspectrum.xml'
        contents = str("""<tool name="rootspectrum" version="$VER"> 
  <info url="http://root.cern.ch/root/"/>
  <lib name="Spectrum"/>
  <use name="roothistmatrix"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rootphysics toolfile
        fname = 'rootphysics.xml'
        contents = str("""<tool name="rootphysics" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Physics"/>
  <use name="roothistmatrix"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# root toolfile, alias for rootphysics. Using rootphysics is preferred.
        fname = 'root.xml'
        contents = str("""<tool name="root" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <use name="rootphysics"/>
  <ifversion name="^[6-9]\.">
    <flags NO_CAPABILITIES="yes"/>
  </ifversion>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rootgpad toolfile
        fname = 'rootgpad.xml'
        contents = str("""<tool name="rootgpad" version="$VER"> 
  <info url="http://root.cern.ch/root/"/>
  <lib name="Gpad"/>
  <lib name="Graf"/>
  <use name="roothistmatrix"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rootgraphics toolfile, identical to old "root" toolfile
        fname = 'rootgraphics.xml'
        contents = str("""<tool name="rootgraphics" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="TreePlayer"/>
  <lib name="Graf3d"/>
  <lib name="Postscript"/>
  <use name="rootgpad"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rooteg toolfile, identical to old "root" toolfile
        fname = 'rooteg.xml'
        contents = str("""<tool name="rooteg" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="EG"/>
  <use name="rootgraphics"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rootpy toolfile, identical to old "root" toolfile
        fname = 'rootpy.xml'
        contents = str("""<tool name="rootpy" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="PyROOT"/>
  <use name="rootgraphics"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rootinteractive toolfile
        fname = 'rootinteractive.xml'
        contents = str("""<tool name="rootinteractive" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Gui"/>
  <use name="libjpeg-turbo"/>
  <use name="libpng"/>
  <use name="rootgpad"/>
  <use name="rootrint"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rootmath toolfile
        fname = 'rootmath.xml'
        contents = str("""<tool name="rootmath" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="GenVector"/>
  <lib name="MathMore"/>
  <use name="rootcore"/>
  <use name="gsl"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rootminuit toolfile
        fname = 'rootminuit.xml'
        contents = str("""<tool name="rootminuit" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Minuit"/>
  <use name="rootgpad"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rootminuit2 toolfile
        fname = 'rootminuit2.xml'
        contents = str("""<tool name="rootminuit2" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Minuit2"/>
  <use name="rootgpad"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rootrflx toolfile
        fname = 'rootrflx.xml'
        contents = str("""<tool name="rootrflx" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <client>
    <environment name="ROOTRFLX_BASE" default="$PFX"/>
  </client>
  <flags GENREFLEX_GCCXMLOPT="-m64"/>
  <flags GENREFLEX_CPPFLAGS="-DCMS_DICT_IMPL -D_REENTRANT -DGNUSOURCE -D__STRICT_ANSI__"/>
  <flags GENREFLEX_ARGS="--deep"/>
  <runtime name="GENREFLEX" value="$PFX/bin/genreflex"/>
  <use name="root_interface"/>
  <use name="rootcling"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# roothtml toolfile
        fname = 'roothtml.xml'
        contents = str("""<tool name="roothtml" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Html"/>
  <use name="rootgpad"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rootmlp toolfile
        fname = 'rootmlp.xml'
        contents = str("""<tool name="rootmlp" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="MLP"/>
  <use name="rootgraphics"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# roottmva toolfile
        fname = 'roottmva.xml'
        contents = str("""<tool name="roottmva" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="TMVA"/>
  <use name="rootmlp"/>
  <use name="rootminuit"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rootxml toolfile
        fname = 'rootxml.xml'
        contents = str("""<tool name="rootxml" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="XMLParser"/>
  <use name="rootcore"/>
  <use name="libxml2"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rootfoam toolfile
        fname = 'rootfoam.xml'
        contents = str("""<tool name="rootfoam" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Foam"/>
  <use name="roothistmatrix"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rootgeom toolfile
        fname = 'rootgeom.xml'
        contents = str("""<tool name="rootgeom" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Geom"/>
  <use name="rootrio"/>
  <use name="rootmathcore"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rootgeompainter toolfile
        fname = 'rootgeompainter.xml'
        contents = str("""<tool name="rootgeompainter" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="GeomPainter"/>
  <use name="rootgeom"/>
  <use name="rootgraphics"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rootrgl toolfile
        fname = 'rootrgl.xml'
        contents = str("""<tool name="rootrgl" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RGL"/>
  <use name="rootinteractive"/>
  <use name="rootgraphics"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rooteve toolfile
        fname = 'rooteve.xml'
        contents = str("""<tool name="rooteve" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Eve"/>
  <use name="rootgeompainter"/>
  <use name="rootrgl"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# rootguihtml toolfile
        fname = 'rootguihtml.xml'
        contents = str("""<tool name="rootguihtml" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="GuiHtml"/>
  <use name="rootinteractive"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# roofitcore toolfile
        fname = 'roofitcore.xml'
        contents = str("""<tool name="roofitcore" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RooFitCore"/>
  <client>
    <environment name="ROOFIT_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$ROOFIT_BASE/lib"/>
    <environment name="INCLUDE" default="$$ROOFIT_BASE/include"/>
  </client>
  <runtime name="ROOFITSYS" value="$$ROOFIT_BASE/"/>
  <runtime name="PATH"      value="$$ROOFIT_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="rootcore"/>
  <use name="roothistmatrix"/>
  <use name="rootgpad"/>
  <use name="rootminuit"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# roofit toolfile
        fname = 'roofit.xml'
        contents = str("""<tool name="roofit" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RooFit"/>
  <use name="roofitcore"/>
  <use name="rootcore"/>
  <use name="rootmath"/>
  <use name="roothistmatrix"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# roostats toolfile
        fname = 'roostats.xml'
        contents = str("""<tool name="roostats" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RooStats"/>
  <use name="roofitcore"/>
  <use name="roofit"/>
  <use name="rootcore"/>
  <use name="roothistmatrix"/>
  <use name="rootgpad"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)


# histfactory toolfile
        fname = 'histfactory.xml'
        contents = str("""<tool name="histfactory" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="HistFactory"/>
  <use name="roofitcore"/>
  <use name="roofit"/>
  <use name="roostats"/>
  <use name="rootcore"/>
  <use name="roothistmatrix"/>
  <use name="rootgpad"/>
  <use name="rootxml"/>
  <use name="rootfoam"/>
</tool>""")
        write_scram_toolfile(contents, values, fname)
